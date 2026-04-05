"""People discovery sources.

Provides adapters for finding relevant contacts at target companies.
Currently provides a mock adapter. Real adapters would use public
professional directories, company team pages, or conference speaker lists.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.schemas.outreach import ContactInput


class PeopleSource(ABC):
    """Abstract base class for people discovery sources."""

    @abstractmethod
    def find_people(self, company_name: str) -> list[ContactInput]:
        """Find relevant contacts at a company. Must not fabricate identities."""
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        ...


class MockPeopleSource(PeopleSource):
    """Mock people source with sample contacts for target companies.

    These represent typical role types you would find at each company.
    Names are illustrative placeholders — replace with real contacts
    discovered through LinkedIn, conferences, or company pages.
    """

    @property
    def source_name(self) -> str:
        return "mock"

    _CONTACTS: dict[str, list[dict]] = {
        "Deere & Company": [
            {
                "name": "[Deere Embedded Hiring Manager]",
                "role": "Embedded Software Manager",
                "company": "Deere & Company",
                "profile_url": "https://www.deere.com/en/our-company/john-deere-careers/",
                "relevance_reason": "Likely manages embedded controls teams; direct hiring authority for embedded roles",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[Deere Technical Recruiter]",
                "role": "Technical Recruiter - Software",
                "company": "Deere & Company",
                "profile_url": "https://www.deere.com/en/our-company/john-deere-careers/",
                "relevance_reason": "Recruiter for embedded/firmware positions at Deere",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[Deere Senior Embedded Engineer]",
                "role": "Senior Embedded Software Engineer",
                "company": "Deere & Company",
                "profile_url": "https://www.deere.com/en/our-company/john-deere-careers/",
                "relevance_reason": "Peer-level connection; can provide insider view of team culture and tech stack",
                "contact_priority": "medium",
                "suggested_outreach_type": "connection",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "CNH Industrial": [
            {
                "name": "[CNH Embedded Engineering Lead]",
                "role": "Embedded Engineering Lead - Sprayers",
                "company": "CNH Industrial",
                "profile_url": "https://careers.cnhindustrial.com/",
                "relevance_reason": "Leads sprayer embedded team; direct relevance to CAN/J1939 + sprayer controls background",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[CNH Recruiter]",
                "role": "Talent Acquisition Specialist",
                "company": "CNH Industrial",
                "profile_url": "https://careers.cnhindustrial.com/",
                "relevance_reason": "Recruiter for engineering positions",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Caterpillar": [
            {
                "name": "[CAT Controls Engineering Manager]",
                "role": "Controls Engineering Manager",
                "company": "Caterpillar",
                "profile_url": "https://www.caterpillar.com/en/careers.html",
                "relevance_reason": "Manages embedded controls team for heavy equipment; CAN/J1939, RTOS background overlap",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[CAT Embedded Engineer]",
                "role": "Embedded Software Engineer",
                "company": "Caterpillar",
                "profile_url": "https://www.caterpillar.com/en/careers.html",
                "relevance_reason": "Peer engineer working on similar embedded problems; warm connection opportunity",
                "contact_priority": "medium",
                "suggested_outreach_type": "warm_engagement_first",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Bosch": [
            {
                "name": "[Bosch Firmware Team Lead]",
                "role": "Firmware Team Lead - Powertrain",
                "company": "Bosch",
                "profile_url": "https://www.bosch.us/careers/",
                "relevance_reason": "Leads automotive firmware team; AUTOSAR, CAN expertise overlap",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[Bosch US Recruiter]",
                "role": "Engineering Recruiter",
                "company": "Bosch",
                "profile_url": "https://www.bosch.us/careers/",
                "relevance_reason": "Handles embedded engineering hiring in US",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Continental": [
            {
                "name": "[Continental ECU Engineering Manager]",
                "role": "ECU Software Engineering Manager",
                "company": "Continental",
                "profile_url": "https://www.continental.com/en/career/",
                "relevance_reason": "Manages ECU firmware teams; CAN/LIN, ARM Cortex, functional safety",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "AGCO Corporation": [
            {
                "name": "[AGCO Controls SW Manager]",
                "role": "Controls Software Manager",
                "company": "AGCO Corporation",
                "profile_url": "https://careers.agcocorp.com/",
                "relevance_reason": "Manages controls SW for ag equipment; MATLAB/Simulink, J1939 — very close to current work",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
            {
                "name": "[AGCO Precision Ag Engineer]",
                "role": "Senior Software Engineer - Precision Ag",
                "company": "AGCO Corporation",
                "profile_url": "https://careers.agcocorp.com/",
                "relevance_reason": "Peer engineer in precision ag; warm connection to learn about AGCO's embedded stack",
                "contact_priority": "medium",
                "suggested_outreach_type": "connection",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Rockwell Automation": [
            {
                "name": "[Rockwell Firmware Manager]",
                "role": "Firmware Engineering Manager",
                "company": "Rockwell Automation",
                "profile_url": "https://www.rockwellautomation.com/en-us/company/careers.html",
                "relevance_reason": "Manages firmware for industrial controllers; FreeRTOS, embedded Linux",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Siemens": [
            {
                "name": "[Siemens Automation Recruiter]",
                "role": "Technical Recruiter - Industrial Automation",
                "company": "Siemens",
                "profile_url": "https://jobs.siemens.com/",
                "relevance_reason": "Handles embedded/automation engineering hiring",
                "contact_priority": "medium",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Semiconductor ──────────────────
        "Qualcomm": [
            {
                "name": "[Qualcomm Firmware Manager]",
                "role": "Firmware Engineering Manager",
                "company": "Qualcomm",
                "profile_url": "https://jobs.qualcomm.com/search-jobs?keywords=embedded",
                "relevance_reason": "Manages embedded firmware teams for wireless SoCs; ARM Cortex, RTOS",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Intel": [
            {
                "name": "[Intel Firmware Manager]",
                "role": "Firmware Engineering Manager",
                "company": "Intel",
                "profile_url": "https://jobs.intel.com/Search/Results?keyword=embedded",
                "relevance_reason": "Manages SoC firmware / BSP teams; embedded Linux, C",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Texas Instruments": [
            {
                "name": "[TI Embedded SW Manager]",
                "role": "Embedded Software Manager - MCU SDK",
                "company": "Texas Instruments",
                "profile_url": "https://careers.ti.com/jobs?keywords=embedded",
                "relevance_reason": "Manages MCU SDK/firmware teams; bare-metal, RTOS, CAN/SPI/I2C",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Analog Devices": [
            {
                "name": "[ADI Firmware Engineer]",
                "role": "Senior Firmware Engineer",
                "company": "Analog Devices",
                "profile_url": "https://www.analog.com/en/about-adi/careers?keywords=embedded",
                "relevance_reason": "Peer engineer in precision sensor firmware; SPI/I2C, DSP",
                "contact_priority": "medium",
                "suggested_outreach_type": "connection",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Infineon": [
            {
                "name": "[Infineon Automotive FW Lead]",
                "role": "Automotive Firmware Team Lead",
                "company": "Infineon",
                "profile_url": "https://infineon.wd3.myworkdayjobs.com/infineonexternal?keywords=embedded",
                "relevance_reason": "Leads AURIX MCU firmware; AUTOSAR, CAN — very close to background",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Broadcom": [
            {
                "name": "[Broadcom Embedded SW Manager]",
                "role": "Embedded Software Engineering Manager",
                "company": "Broadcom",
                "profile_url": "https://careers.broadcom.com/jobs?keywords=embedded",
                "relevance_reason": "Manages networking ASIC firmware teams; Linux, C",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Samsung Semiconductor": [
            {
                "name": "[Samsung SoC FW Manager]",
                "role": "SoC Firmware Engineering Manager",
                "company": "Samsung Semiconductor",
                "profile_url": "https://semiconductor.samsung.com/us/careers/search?keyword=embedded",
                "relevance_reason": "Manages SoC firmware; embedded Linux, ARM TrustZone",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "ARM": [
            {
                "name": "[ARM Embedded SW Lead]",
                "role": "Embedded Software Lead - Processor Validation",
                "company": "ARM",
                "profile_url": "https://arm.wd1.myworkdayjobs.com/ARM_Careers/jobs?keywords=embedded",
                "relevance_reason": "Leads embedded SW team for Cortex validation; C/C++, RTOS, JTAG",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Automotive ──────────────────────
        "Aptiv": [
            {
                "name": "[Aptiv ADAS FW Manager]",
                "role": "ADAS Firmware Engineering Manager",
                "company": "Aptiv",
                "profile_url": "https://aptiv.avature.net/careers?keyword=embedded",
                "relevance_reason": "Manages ADAS embedded software; CAN, AUTOSAR, sensor fusion",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Ford Motor Company": [
            {
                "name": "[Ford EV Controls Manager]",
                "role": "EV Powertrain Controls Manager",
                "company": "Ford Motor Company",
                "profile_url": "https://corporate.ford.com/careers/all-jobs.html?keywords=embedded",
                "relevance_reason": "Manages EV embedded controls; CAN, MATLAB/Simulink, model-based dev",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "General Motors": [
            {
                "name": "[GM Embedded SW Manager]",
                "role": "Embedded Software Engineering Manager",
                "company": "General Motors",
                "profile_url": "https://search-careers.gm.com/search-jobs?keywords=embedded",
                "relevance_reason": "Manages vehicle embedded SW teams; CAN, AUTOSAR, Linux",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Magna International": [
            {
                "name": "[Magna ECU FW Lead]",
                "role": "ECU Firmware Team Lead",
                "company": "Magna International",
                "profile_url": "https://careers.magna.com/search?keywords=embedded",
                "relevance_reason": "Leads vehicle ECU firmware; CAN, AUTOSAR, ISO 26262",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Cummins": [
            {
                "name": "[Cummins Controls Manager]",
                "role": "Embedded Controls Engineering Manager",
                "company": "Cummins",
                "profile_url": "https://jobs.cummins.com/search-jobs?keywords=embedded",
                "relevance_reason": "Manages engine embedded controls; CAN/J1939, MATLAB/Simulink — very relevant",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Tesla": [
            {
                "name": "[Tesla Firmware Recruiter]",
                "role": "Technical Recruiter - Firmware",
                "company": "Tesla",
                "profile_url": "https://www.tesla.com/careers/search?keywords=embedded",
                "relevance_reason": "Recruiter for firmware/embedded positions",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Lucid Motors": [
            {
                "name": "[Lucid Drivetrain FW Lead]",
                "role": "Drivetrain Firmware Lead",
                "company": "Lucid Motors",
                "profile_url": "https://lucidgroup.icims.com/jobs/search?searchKeyword=embedded",
                "relevance_reason": "Leads EV drivetrain firmware; motor control, CAN, RTOS",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "ZF Group": [
            {
                "name": "[ZF Embedded SW Manager]",
                "role": "Embedded Software Manager - Transmission",
                "company": "ZF Group",
                "profile_url": "https://jobs.zf.com/search-jobs?keywords=embedded",
                "relevance_reason": "Manages transmission embedded controls; CAN, AUTOSAR, MATLAB/Simulink",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Aerospace & Defense ─────────────
        "Boeing": [
            {
                "name": "[Boeing Avionics FW Manager]",
                "role": "Avionics Software Manager",
                "company": "Boeing",
                "profile_url": "https://jobs.boeing.com/search-jobs?keywords=embedded",
                "relevance_reason": "Manages avionics firmware; DO-178C, RTOS, Ada/C",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Lockheed Martin": [
            {
                "name": "[LM Embedded SW Lead]",
                "role": "Embedded Software Engineering Lead",
                "company": "Lockheed Martin",
                "profile_url": "https://jobs.lockheedmartin.com/search-jobs?keywords=embedded",
                "relevance_reason": "Leads mission-critical embedded teams; RTOS, C/C++",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Raytheon Technologies": [
            {
                "name": "[RTX Firmware Manager]",
                "role": "Firmware Engineering Manager - Radar",
                "company": "Raytheon Technologies",
                "profile_url": "https://www.rtx.com/careers/job-search?keywords=embedded",
                "relevance_reason": "Manages radar firmware teams; FPGA, DSP, RTOS",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Northrop Grumman": [
            {
                "name": "[NG Embedded SW Manager]",
                "role": "Embedded Systems Engineering Manager",
                "company": "Northrop Grumman",
                "profile_url": "https://www.northropgrumman.com/careers/job-search?searchTerm=embedded",
                "relevance_reason": "Manages defense embedded systems; RTOS, VxWorks, DO-178C",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "GE Aerospace": [
            {
                "name": "[GE FADEC SW Manager]",
                "role": "FADEC Software Manager",
                "company": "GE Aerospace",
                "profile_url": "https://jobs.gecareers.com/jobs?keywords=embedded",
                "relevance_reason": "Manages engine control firmware; DO-178C, RTOS, model-based dev",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Robotics & Consumer ─────────────
        "Boston Dynamics": [
            {
                "name": "[BD Embedded Robotics Lead]",
                "role": "Embedded Software Lead - Robotics",
                "company": "Boston Dynamics",
                "profile_url": "https://jobs.smartrecruiters.com/BostonDynamics?keywords=embedded",
                "relevance_reason": "Leads robot embedded systems; motor control, real-time Linux, CAN",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "DJI": [
            {
                "name": "[DJI Flight Controller FW Lead]",
                "role": "Flight Controller Firmware Lead",
                "company": "DJI",
                "profile_url": "https://careers-dji.icims.com/jobs/search?searchKeyword=embedded",
                "relevance_reason": "Leads drone flight controller firmware; ARM, RTOS, sensor fusion",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "ABB": [
            {
                "name": "[ABB Robotics FW Manager]",
                "role": "Firmware Engineering Manager - Robotics",
                "company": "ABB",
                "profile_url": "https://careers.abb/global/en/search-results?keywords=embedded",
                "relevance_reason": "Manages robotics firmware; motor control, CAN, industrial Ethernet",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Networking ──────────────────────
        "Cisco Systems": [
            {
                "name": "[Cisco Embedded SW Manager]",
                "role": "Embedded Software Engineering Manager",
                "company": "Cisco Systems",
                "profile_url": "https://jobs.cisco.com/",
                "relevance_reason": "Manages switch/router embedded OS teams; Linux, C, ASIC drivers",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Arista Networks": [
            {
                "name": "[Arista EOS FW Lead]",
                "role": "EOS Platform Engineering Lead",
                "company": "Arista Networks",
                "profile_url": "https://www.arista.com/en/company/careers?keywords=embedded",
                "relevance_reason": "Leads network OS embedded development; Linux, C/C++",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        # ── H1B Sponsor Companies - Big Tech ────────────────────────
        "Apple": [
            {
                "name": "[Apple HW FW Recruiter]",
                "role": "Technical Recruiter - Hardware Firmware",
                "company": "Apple",
                "profile_url": "https://jobs.apple.com/en/search?keywords=embedded",
                "relevance_reason": "Recruiter for hardware firmware positions",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Google": [
            {
                "name": "[Google HW FW Manager]",
                "role": "Firmware Engineering Manager - Hardware",
                "company": "Google",
                "profile_url": "https://careers.google.com/jobs/results/?q=embedded",
                "relevance_reason": "Manages Pixel/Nest firmware teams; embedded Linux, C/C++",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Meta": [
            {
                "name": "[Meta AR/VR FW Manager]",
                "role": "Firmware Engineering Manager - Reality Labs",
                "company": "Meta",
                "profile_url": "https://www.metacareers.com/jobs?keywords=embedded",
                "relevance_reason": "Manages AR/VR headset firmware; sensors, RTOS, BLE",
                "contact_priority": "high",
                "suggested_outreach_type": "hiring_manager_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
        "Amazon": [
            {
                "name": "[Amazon Devices FW Recruiter]",
                "role": "Technical Recruiter - Device Firmware",
                "company": "Amazon",
                "profile_url": "https://www.amazon.jobs/en/search?keywords=embedded+firmware",
                "relevance_reason": "Recruiter for Echo/Ring/Kindle firmware positions",
                "contact_priority": "high",
                "suggested_outreach_type": "recruiter_intro",
                "source": "mock — replace with real contact from LinkedIn",
            },
        ],
    }

    def find_people(self, company_name: str) -> list[ContactInput]:
        contacts_data = self._CONTACTS.get(company_name, [])
        return [ContactInput(**c) for c in contacts_data]


# TODO: Implement PublicDirectoryPeopleSource
# This source would:
# 1. Check company team / about pages for publicly listed team members
# 2. Scan conference speaker lists for engineers at target companies
# 3. Parse public GitHub org member lists
# 4. Respect privacy — only use publicly available information
#
# class PublicDirectoryPeopleSource(PeopleSource):
#     ...


def get_people_source() -> PeopleSource:
    """Return the configured people source."""
    return MockPeopleSource()
