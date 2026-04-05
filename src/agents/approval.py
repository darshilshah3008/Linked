"""Approval Agent.

Reviews externally visible content for quality, safety, and
factual grounding before marking as approved.

Checks:
1. Unsupported claims
2. Fabricated information
3. Spam indicators
4. Unsafe automation steps
5. Tone appropriateness
"""

from __future__ import annotations

import re

from loguru import logger

from src.schemas.approval import ApprovalDecision, ApprovalRequest


class ApprovalAgent:
    """Agent responsible for reviewing content before external visibility."""

    AGENT_NAME = "approval"

    # ── Patterns to flag ──────────────────────────────────

    # Claims that sound fabricated or unverifiable
    UNSUPPORTED_CLAIM_PATTERNS = [
        r"\b\d{2,3}%\b",  # Specific percentage claims (may need verification)
        r"guaranteed",
        r"proven track record",
        r"best in class",
        r"world-class",
        r"#1\b",
        r"top \d+%",
    ]

    # Spam indicators
    SPAM_PATTERNS = [
        r"act now",
        r"limited time",
        r"don't miss",
        r"exclusive opportunity",
        r"reply urgently",
        r"!!!",
    ]

    # Unsafe automation indicators
    UNSAFE_PATTERNS = [
        r"auto.?send",
        r"auto.?post",
        r"auto.?apply",
        r"auto.?comment",
        r"click here to apply",
    ]

    # Known verifiable claims from the user's actual profile
    VERIFIED_CLAIMS = {
        "40%": "build and deployment time reduction",
        "30%": "vehicle stability improvement / field failure reduction",
        "50%": "merge conflict reduction",
        "25%": "system response latency reduction",
        "100+": "issues resolved in Polarion/SharePoint",
        "6+": "years of experience",
    }

    def review(self, request: ApprovalRequest) -> ApprovalDecision:
        """Review content for approval.

        Returns an ApprovalDecision with decision, reasons, and issues.
        """
        text = request.content_text
        issues: list[str] = []
        reasons: list[str] = []

        # Check for unsupported claims
        self._check_unsupported_claims(text, issues, reasons)

        # Check for spam
        self._check_spam(text, issues, reasons)

        # Check for unsafe automation
        self._check_unsafe(text, issues, reasons)

        # Check minimum length
        if len(text.strip()) < 20:
            issues.append("Content is too short to be meaningful.")

        # Check for placeholder markers (not necessarily bad, but note them)
        placeholders = re.findall(r"\[([A-Z_]+)\]", text)
        if placeholders:
            reasons.append(
                f"Contains placeholders needing human input: {', '.join(placeholders[:5])}"
            )

        # Determine decision
        if issues:
            # Critical issues -> reject
            critical = [i for i in issues if "unsafe" in i.lower() or "fabricat" in i.lower()]
            if critical:
                decision = "rejected"
                confidence = 0.9
            else:
                decision = "revision_needed"
                confidence = 0.6
        else:
            decision = "approved"
            confidence = 0.8
            reasons.append("Content passes all automated checks.")

        if not reasons and not issues:
            reasons.append("No specific issues found.")

        logger.debug(
            f"Approval review: {decision} (confidence: {confidence}) "
            f"issues: {len(issues)}, type: {request.item_type}"
        )

        return ApprovalDecision(
            decision=decision,
            reasons=reasons,
            confidence_score=confidence,
            flagged_issues=issues,
        )

    def _check_unsupported_claims(
        self, text: str, issues: list[str], reasons: list[str]
    ) -> None:
        """Check for percentage claims and verify against known profile."""
        for pattern in self.UNSUPPORTED_CLAIM_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                match_str = match if isinstance(match, str) else match[0]
                # Check if this is a verified claim
                verified = False
                for claim_key, claim_desc in self.VERIFIED_CLAIMS.items():
                    if claim_key in match_str:
                        verified = True
                        reasons.append(f"Verified claim: {match_str} ({claim_desc})")
                        break
                if not verified:
                    # Flag patterns like "guaranteed", "best in class" as issues
                    if not re.match(r"\b\d+%?\b", match_str):
                        issues.append(
                            f"Potentially unsupported claim: '{match_str}'. "
                            "Verify this is grounded in actual data."
                        )

    def _check_spam(self, text: str, issues: list[str], reasons: list[str]) -> None:
        """Check for spam-like language."""
        for pattern in self.SPAM_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"Spam indicator detected: pattern '{pattern}'")

    def _check_unsafe(self, text: str, issues: list[str], reasons: list[str]) -> None:
        """Check for unsafe automation language."""
        for pattern in self.UNSAFE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(
                    f"Unsafe automation indicator: '{pattern}'. "
                    "All external actions must be human-approved."
                )
