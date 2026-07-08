#!/usr/bin/env python3
"""Daily Morning Brief (cloud, Claude API).

One email, every morning, with two things Darshil actually uses day to day:
  1. Today's ready-to-post LinkedIn post (LLM-written, weekday-rotated pillar)
     + a navy quote-card poster attached as PNG.
  2. A live AI news digest (Claude API web search over the last ~24h).

This consolidates the two earlier scripts into a single run/email. Nothing is
posted to LinkedIn automatically — you review the email and publish manually.

Recommended home: commit to ONE repo (e.g. AI_news) at:
  scripts/daily_brief.py
and schedule it with the daily-brief.yml workflow.

Required environment variables (GitHub Actions repo secrets):
  ANTHROPIC_API_KEY  - your Anthropic API key (https://console.anthropic.com)
  SMTP_USER          - sending Gmail address, e.g. you@gmail.com
  SMTP_PASS          - a Gmail App Password (16 chars), NOT your login password
  EMAIL_TO           - where to send it, e.g. darshilshah3008@gmail.com
"""

import os
import re
import json
import ssl
import smtplib
import datetime
from email.message import EmailMessage

import anthropic
from PIL import Image, ImageDraw, ImageFont

MODEL = "claude-sonnet-5"

PROFILE = """
Name: Darshil Shah
Role: Embedded Software / Firmware Engineer, with a strong interest in edge AI
and AI developer tooling.
Core expertise: embedded systems; firmware in C/C++; RTOS (esp. FreeRTOS);
CAN bus & J1939 vehicle networking; embedded CI/CD and hardware-in-the-loop
testing; model-based development (MATLAB/Simulink); field reliability;
industrial/automotive/agricultural embedded.
Edge AI interest: on-device inference (NVIDIA Jetson/Orin), TensorRT, ONNX,
quantization.
Real topics he actually posts about (from his LinkedIn): embedded systems,
firmware engineering, edge AI, running local AI on NVIDIA Jetson Orin Nano,
local RAG / on-device LLMs, automotive embedded engineering, and debugging.
He is active in IEEE-HKN.
Builds in public: a local RAG + LLM benchmark project (on his GitHub), plus
"Job Search Copilot" and "AI Signal OS". He likes benchmarking and running AI
locally on constrained hardware.
Goal on LinkedIn: build credibility and a following by sharing genuinely useful
work, findings, and lessons — as a builder, not a job seeker.
Never fabricate specific metrics or achievements not implied above.
""".strip()

# Two of Darshil's REAL posts. Match this exact voice, rhythm, and structure.
STYLE_SAMPLES = """
--- SAMPLE 1 ---
My LLM crashed with "out of memory" while showing several GB free. That bug, and
one bad character, taught me more about edge AI than any model benchmark ever could.

I bought a Jetson Orin Nano to run an LLM fully offline. As an embedded engineer,
the two walls I hit had almost nothing to do with AI. One was memory architecture,
the other a single apostrophe. Both felt like home.

Wall #1: living inside an 8 GB memory budget. cudaMalloc died with "out of memory"
while GB were supposedly free. The driver log told the truth: NvMap error 12 (ENOMEM).
The Orin Nano uses unified memory — CPU and GPU share one 8 GB pool, and default
mmap loaded the weights twice. Fix: use_mmap:false, a userspace cache evictor, one
model resident at a time, a bounded context window.

Wall #2: an HTTP 500 that was really a NaN. The embedder emitted a NaN vector
whenever the input contained an apostrophe: 5/5 failures with one, 0/5 without.
Fix: strip apostrophes from the embedding input only.

The lesson: read one layer below the symptom, and let the data name the cause.

The edge-AI gap usually isn't the model. It's the systems discipline around it.
That's embedded work. And it transfers directly.

What's the gnarliest "it's not the model, it's the system" bug you've hit?

--- SAMPLE 2 ---
Firmware engineer here. CAN, J1939, RTOS, automotive embedded work where timing
errors aren't bugs, they're incidents. That's my day job.

On the side I've been running Mistral 7B on a Jetson Orin Nano. Local RAG pipeline.
NVMe storage. 4 watts. No cloud, no API keys, no internet required. Not a demo.
Actually works.

Here's why I think this matters:
→ Diagnostics that run inside the ECU, not some AWS server farm
→ Operator assist that doesn't die when you lose cell signal
→ Sensor anomaly detection where the data stays on the vehicle

Embedded engineers already think in deadlines, power budgets, and failure modes.
That mindset translates directly to edge AI.

CAN + inference. RTOS + quantization. Hardware integration + edge deployment.
""".strip()

PILLARS = {
    0: "Firmware / embedded software deep-dive (C/C++, RTOS/FreeRTOS, drivers, memory, real-time, CAN/J1939): a lesson he figured out that others can use.",
    1: "LLMs in practice: something he did with LLMs (running them locally/on-device, agents, prompting, evals, tooling) and what he learned.",
    2: "Building in public: what he's building right now with firmware or LLMs, why, and an interesting finding.",
    3: "A firmware/embedded debugging story and the concrete takeaway other engineers can steal.",
    4: "Where LLMs meet embedded/edge: on-device inference, LLMs on constrained hardware, TensorRT/ONNX/quantization — a practical insight.",
    5: "A practical tip or mini-tutorial in firmware, embedded, or LLM tooling that saves time.",
    6: "Something he learned this week in firmware, embedded, or LLMs worth passing on.",
}
ACCENTS = {
    0: "#36D1C4", 1: "#F2A03D", 2: "#6C8CFF", 3: "#E8623D",
    4: "#4FC3E8", 5: "#7BD88F", 6: "#C78BFF",
}


# ---------- LinkedIn post ----------------------------------------------------
def find_trend(client, pillar):
    """Best-effort: one recent development to anchor the post. Never raises."""
    try:
        msg = client.messages.create(
            model=MODEL, max_tokens=700,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 4}],
            messages=[{"role": "user", "content": (
                "Search the web for ONE genuinely recent (last ~2 weeks) real "
                f"development relevant to: {pillar}\n\n"
                "Reply with 2-3 plain sentences: what it is and why it matters. "
                "No preamble, no markdown."
            )}],
        )
        return "".join(b.text for b in msg.content
                       if getattr(b, "type", None) == "text").strip()
    except Exception:  # noqa: BLE001
        return ""


def generate_post(client, pillar, trend=""):
    system = (
        "You write LinkedIn posts AS Darshil Shah, a real embedded software "
        "engineer. You are not a marketer. Every post must sound like one "
        "specific human talking, grounded ONLY in his real background below. "
        "Never invent metrics or achievements.\n\n" + PROFILE + "\n\n"
        "POSITIONING: He is SHARING what he's building and learning to be useful "
        "and interesting to other engineers. He is NOT looking for a job, NOT "
        "asking for anything, NOT selling himself. Never frame a post around job "
        "hunting, recruiters, hiring, or 'looking for opportunities'. The vibe is "
        "a builder thinking out loud, not a candidate.\n\n"
        "VOICE (blend of two things every post):\n"
        "1) Personal & specific: open with a real moment, observation, or a "
        "concrete thing he did/noticed — not a generic thesis.\n"
        "2) Practical: land on ONE useful, concrete takeaway another engineer "
        "can actually apply.\n\n"
        "HARD RULES:\n"
        "- Sentence case everywhere. NEVER Title Case.\n"
        "- Emoji: restrained and functional only. Use '→' for structured points "
        "(he does this often). At most one or two simple markers if genuinely "
        "useful. NEVER hype emoji (no rockets, gems, wrenches, sparkles) and "
        "never bold-unicode headers.\n"
        "- Banned phrases: 'I'm humbled', 'excited to share', 'game-changer', "
        "'in today's fast-paced world', 'the power of', 'thrilled', 'delve', "
        "'dive in', 'unlock', 'leverage'. Avoid anything that smells AI-generated.\n"
        "- Short sentences. Concrete nouns. Real specifics (actual error messages, "
        "numbers, commands) over buzzwords — like the samples.\n"
        "- Admit limitations honestly when it fits ('engineer's honesty').\n"
        "- No humble-brag. Confident but plain-spoken.\n\n"
        "STYLE REFERENCE — match the voice, rhythm, and structure of these real "
        "posts by Darshil:\n\n" + STYLE_SAMPLES + "\n"
    )
    hook_note = (
        "A recent, real development you MAY use as a timely hook — only if it "
        f"fits naturally with his experience:\n{trend}\n\n"
    ) if trend else ""
    user = f"""Write ONE LinkedIn post for today. Angle for today: {pillar}

{hook_note}Write the post as Darshil's OWN take, grounded in his real experience.
If the development above fits, hook onto it; otherwise write from his own work.
It is NOT a news summary.

Caption requirements:
- Length 80-160 words. Tight. Cut every word that isn't earning its place.
- First line is a real hook: specific, conversational, sentence case.
- Short paragraphs / line breaks; use → for lists like he does.
- Ground it in his real work (firmware, RTOS, CAN/J1939, on-device LLMs/edge AI,
  his side projects). One genuine takeaway.
- End with a real question that invites a reply.
- 3-4 relevant hashtags on the last line.

Respond with ONLY valid JSON (no fences, no markdown):
{{"kicker":"SHORT UPPERCASE LABEL for the poster, sharing-oriented e.g. FIELD NOTES, EDGE AI, BUILD LOG (never job/hiring words)","poster_headline":"5-9 word distillation of the hook, in SENTENCE CASE (only first word + proper nouns capitalized)","poster_subtitle":"one short supporting line, under 8 words, sentence case","caption":"the full post text exactly as it should be pasted"}}"""
    msg = client.messages.create(
        model=MODEL, max_tokens=1600, system=system,
        messages=[{"role": "user", "content": user}],
    )
    raw = "".join(b.text for b in msg.content if b.type == "text").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group(0)
    if not raw:
        raise RuntimeError("Model returned no JSON for the post.")
    return json.loads(raw)


# ---------- AI news digest ---------------------------------------------------
def generate_news(client):
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    prompt = f"""Today is {today}. Build a high-signal digest of the most
important AI developments from the LAST 24-48 HOURS. Use web search to find and
verify current items across: major model/product releases; notable research and
benchmarks; new AI developer tools/agents; funding & business moves; policy &
safety. Pick 6-9 recent, verified items ranked by importance.

Return ONLY an HTML fragment (no wrapper, no fences): start with one
<p><strong>Why it matters today:</strong> ...</p>; group items under short <h3>
headers; each item is a <p> with a <strong>headline</strong>, a 1-2 sentence
summary, and an <a href="URL">source</a>. Skimmable in under 3 minutes."""
    msg = client.messages.create(
        model=MODEL, max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}],
        messages=[{"role": "user", "content": prompt}],
    )
    html = "".join(b.text for b in msg.content if b.type == "text").strip()
    return re.sub(r"^```(?:html)?|```$", "", html.strip(), flags=re.MULTILINE).strip()


# ---------- Poster -----------------------------------------------------------
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render_poster(headline, kicker, subtitle, accent_hex, out_path):
    W = H = 1080
    NAVY, WHITE, MUTE, LINE = (10, 31, 68), (238, 242, 248), (142, 160, 188), (30, 58, 99)
    accent = hex_to_rgb(accent_hex)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # thin border frame
    d.rectangle([64, 64, W - 64, H - 64], outline=LINE, width=2)
    # monogram top-right
    d.ellipse([W - 150, 68, W - 74, 144], outline=accent, width=3)
    mono = ImageFont.truetype(bold, 30)
    mw = d.textlength("DS", font=mono)
    d.text((W - 112 - mw / 2, 92), "DS", font=mono, fill=accent)

    # accent bar + kicker
    d.rectangle([100, 168, 168, 178], fill=accent)
    d.text((100, 208), (kicker or "FIELD NOTES").upper(),
           font=ImageFont.truetype(bold, 28), fill=accent)

    # headline (capitalize first letter, wrap, accent the last line(s))
    headline = (headline or "").strip()
    if headline:
        headline = headline[0].upper() + headline[1:]
    fh = ImageFont.truetype(bold, 74)
    max_w, words, lines, cur = W - 240, headline.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fh) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = 300
    for i, ln in enumerate(lines):
        color = accent if (len(lines) > 1 and i == len(lines) - 1) else WHITE
        d.text((100, y), ln, font=fh, fill=color)
        y += 88

    # divider + subtitle
    d.line([(100, y + 12), (250, y + 12)], fill=LINE, width=2)
    if subtitle:
        d.text((100, y + 34), subtitle, font=ImageFont.truetype(reg, 27), fill=MUTE)

    # footer
    d.rectangle([100, H - 164, 106, H - 104], fill=accent)
    d.text((124, H - 162), "Darshil Shah", font=ImageFont.truetype(bold, 38), fill=WHITE)
    d.text((124, H - 116), "Embedded Software Engineer  -  Edge AI",
           font=ImageFont.truetype(reg, 25), fill=MUTE)
    img.save(out_path)
    return out_path


# ---------- Email ------------------------------------------------------------
def send_brief(caption, kicker, news_html, poster_path):
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    to_addr = os.environ["EMAIL_TO"]
    today = datetime.date.today().strftime("%a, %b %d")

    msg = EmailMessage()
    msg["Subject"] = f"Morning Brief - {today}"
    msg["From"] = smtp_user
    msg["To"] = to_addr

    text = (
        f"MORNING BRIEF - {today}\n\n"
        f"1) TODAY'S LINKEDIN POST ({kicker}) - copy the caption below, attach the poster.\n\n"
        f"{caption}\n\n"
        "----------------------------------------\n\n"
        "2) AI NEWS DIGEST\n\n"
        f"{re.sub(r'<[^>]+>', '', news_html)}\n"
    )
    msg.set_content(text)

    caption_html = caption.replace("\n", "<br>")
    html_doc = f"""<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#1a1a1a;max-width:660px">
      <h2 style="margin:0 0 4px">Morning Brief &middot; {today}</h2>
      <div style="background:#0A1F44;color:#EEF2F8;padding:16px 18px;border-radius:12px;margin:14px 0">
        <div style="font-size:12px;letter-spacing:1px;color:#8ea0bc;margin-bottom:6px">TODAY'S LINKEDIN POST &middot; {kicker}</div>
        <div style="white-space:pre-wrap;font-size:15px">{caption_html}</div>
        <div style="font-size:12px;color:#8ea0bc;margin-top:10px">Poster attached as PNG. Copy the text above into LinkedIn, then upload the poster.</div>
      </div>
      <h3 style="margin:22px 0 6px">AI news digest</h3>
      {news_html}
      <hr style="border:none;border-top:1px solid #ddd;margin:20px 0">
      <p style="color:#888;font-size:12px">Generated automatically via the Claude API.</p>
    </div>"""
    msg.add_alternative(html_doc, subtype="html")

    with open(poster_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png",
                           filename=os.path.basename(poster_path))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)


def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    weekday = datetime.date.today().weekday()
    pillar, accent = PILLARS[weekday], ACCENTS[weekday]

    trend = find_trend(client, pillar)
    post = generate_post(client, pillar, trend)
    kicker = post.get("kicker", "FIELD NOTES")
    headline = post.get("poster_headline") or post["caption"].split("\n")[0]
    subtitle = post.get("poster_subtitle", "")
    caption = post["caption"]

    # If news fails, still send the LinkedIn post rather than nothing.
    try:
        news_html = generate_news(client)
    except Exception as e:  # noqa: BLE001
        news_html = f"<p>(AI news digest unavailable today: {e})</p>"
    if not news_html.strip():
        news_html = "<p>(No fresh AI news was pulled this run.)</p>"

    date_str = datetime.date.today().isoformat()
    poster = render_poster(headline, kicker, subtitle, accent, f"poster-{date_str}.png")
    send_brief(caption, kicker, news_html, poster)
    print(f"Sent Morning Brief {date_str} | pillar {weekday} | accent {accent}")


if __name__ == "__main__":
    main()
