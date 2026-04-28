"""Lead source adapters.

Implements an adapter pattern so lead sources are swappable.
Currently provides:
- MockLeadSource: returns sample leads for testing/development
- PublicCareersPageAdapter: TODO stub for scraping company career pages
- RSSJobSourceAdapter: TODO stub for RSS/Atom job feeds
"""

from __future__ import annotations

import os

from abc import ABC, abstractmethod

from src.schemas.lead import LeadInput


class LeadSource(ABC):
    """Abstract base class for lead sources."""

    @abstractmethod
    def fetch_leads(self, keywords: list[str], location: str | None = None) -> list[LeadInput]:
        """Fetch leads matching keywords. Must not fabricate data."""
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of this source."""
        ...


class MockLeadSource(LeadSource):
    """Mock lead source returning sample data for development/testing.

    These are illustrative leads based on real companies known to hire
    embedded engineers. URLs point to real public career pages where
    listed; None where not confirmed.
    """

    @property
    def source_name(self) -> str:
        return "mock"

    def fetch_leads(self, keywords: list[str], location: str | None = None) -> list[LeadInput]:
        return [
            # ── Original core leads ─────────────────────────────────
            LeadInput(
                title="Senior Embedded Software Engineer",
                company="Deere & Company",
                location="Moline, IL",
                source="mock",
                url="https://jobs.deere.com/search-jobs?keywords=embedded",
                description_snippet="Design embedded control systems for agricultural equipment. "
                "Experience with CAN/J1939, RTOS, and C/C++ required.",
            ),
            LeadInput(
                title="Firmware Engineer - Industrial Controls",
                company="Rockwell Automation",
                location="Milwaukee, WI",
                source="mock",
                url="https://www.rockwellautomation.com/en-us/company/careers.html",
                description_snippet="Develop firmware for industrial automation controllers. "
                "SPI, I2C, FreeRTOS experience preferred.",
            ),
            LeadInput(
                title="Embedded Systems Engineer",
                company="Oshkosh Corporation",
                location="Oshkosh, WI",
                source="mock",
                url="https://oshkoshcorporation.jobs/",
                description_snippet="Work on vehicle control systems for specialty vehicles. "
                "CAN bus, embedded Linux, C/C++.",
            ),
            LeadInput(
                title="Controls Software Engineer",
                company="AGCO Corporation",
                location="Hesston, KS",
                source="mock",
                url="https://careers.agcocorp.com/",
                description_snippet="Develop control algorithms for agricultural sprayers. "
                "MATLAB/Simulink, J1939, embedded C.",
            ),
            LeadInput(
                title="Embedded Software Developer",
                company="Parker Hannifin",
                location="Cleveland, OH",
                source="mock",
                url="https://www.parker.com/careers",
                description_snippet="Firmware development for hydraulic control systems. "
                "FreeRTOS, CAN, safety-critical systems.",
            ),
            LeadInput(
                title="Senior Firmware Engineer",
                company="Honeywell",
                location="Remote, USA",
                source="mock",
                url="https://careers.honeywell.com/jobs?keywords=embedded",
                description_snippet="IoT edge device firmware. BLE, embedded Linux, "
                "sensor integration, CI/CD pipelines.",
            ),
            LeadInput(
                title="Embedded Software Engineer II",
                company="Caterpillar",
                location="Peoria, IL",
                source="mock",
                url="https://www.caterpillar.com/en/careers.html",
                description_snippet="Embedded controls for heavy machinery. "
                "CAN/J1939, STM32, RTOS, model-based development.",
            ),
            LeadInput(
                title="Software Engineer - Embedded Systems",
                company="Medtronic",
                location="Minneapolis, MN",
                source="mock",
                url="https://jobs.medtronic.com/",
                description_snippet="Medical device embedded software. "
                "C/C++, RTOS, safety-critical development, SPI/I2C.",
            ),
            LeadInput(
                title="Senior Embedded Controls Engineer",
                company="CNH Industrial",
                location="Racine, WI",
                source="mock",
                url="https://careers.cnhindustrial.com/",
                description_snippet="Develop embedded control software for agricultural sprayers "
                "and tractors. CAN/J1939, MATLAB/Simulink, C/C++, CI/CD.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Automotive",
                company="Bosch",
                location="Plymouth, MI",
                source="mock",
                url="https://www.bosch.us/careers/search/?keywords=embedded",
                description_snippet="Automotive embedded software for powertrain and chassis systems. "
                "AUTOSAR, CAN, embedded C, unit testing. Python scripting a plus.",
            ),
            LeadInput(
                title="Firmware Developer - Vehicle Electronics",
                company="Continental",
                location="Auburn Hills, MI",
                source="mock",
                url="https://jobs-continental.icims.com/jobs/search?searchKeyword=embedded",
                description_snippet="Vehicle electronics firmware development. "
                "ARM Cortex, CAN/LIN, RTOS, functional safety (ISO 26262).",
            ),
            LeadInput(
                title="Controls Engineer - Precision Agriculture",
                company="Siemens",
                location="Remote, USA",
                source="mock",
                url="https://jobs.siemens.com/",
                description_snippet="PLC and embedded controls for industrial automation. "
                "SCADA, industrial Ethernet, embedded Linux.",
            ),
            # ── H1B Sponsor Companies - Semiconductor / Chip ────────
            LeadInput(
                title="Embedded Firmware Engineer",
                company="Qualcomm",
                location="San Diego, CA",
                source="mock",
                url="https://jobs.qualcomm.com/search-jobs?keywords=embedded",
                description_snippet="Embedded firmware for wireless SoCs. ARM Cortex-M/A, "
                "RTOS, Bluetooth/WiFi stacks, C/C++, low-power optimization.",
            ),
            LeadInput(
                title="Firmware Engineer - SoC Bring-up",
                company="Intel",
                location="Hillsboro, OR",
                source="mock",
                url="https://jobs.intel.com/Search/Results?keyword=embedded",
                description_snippet="SoC firmware bring-up, BIOS/UEFI, embedded Linux BSP, "
                "C/C++, hardware-software integration, lab debugging.",
            ),
            LeadInput(
                title="Embedded Software Engineer - MCU",
                company="Texas Instruments",
                location="Dallas, TX",
                source="mock",
                url="https://careers.ti.com/jobs?keywords=embedded",
                description_snippet="Develop SDK and firmware for TI MCUs. Bare-metal and RTOS, "
                "CAN, SPI, I2C, ADC drivers. C/C++, ARM Cortex-M.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Sensors",
                company="Analog Devices",
                location="Wilmington, MA",
                source="mock",
                url="https://www.analog.com/en/about-adi/careers?keywords=embedded",
                description_snippet="Embedded firmware for precision sensor ICs. SPI/I2C drivers, "
                "signal conditioning, DSP algorithms, low-power design.",
            ),
            LeadInput(
                title="Firmware Engineer - Automotive MCU",
                company="Infineon",
                location="San Jose, CA",
                source="mock",
                url="https://infineon.wd3.myworkdayjobs.com/infineonexternal?keywords=embedded",
                description_snippet="Automotive MCU firmware. AUTOSAR MCAL, CAN/LIN, "
                "functional safety ISO 26262, embedded C, ARM Cortex.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Storage",
                company="Micron Technology",
                location="Boise, ID",
                source="mock",
                url="https://jobs.micron.com/search?keyword=embedded",
                description_snippet="Firmware for NAND/DRAM controllers. Embedded C/C++, "
                "RTOS, DMA, performance optimization, hardware validation.",
            ),
            LeadInput(
                title="Firmware Engineer - SSD Controller",
                company="Western Digital",
                location="Milpitas, CA",
                source="mock",
                url="https://jobs.westerndigital.com/search-jobs?keywords=embedded",
                description_snippet="SSD controller firmware development. C/C++, RTOS, "
                "flash management, NVMe protocol, ARM-based platforms.",
            ),
            LeadInput(
                title="Firmware Engineer - HDD",
                company="Seagate Technology",
                location="Shakopee, MN",
                source="mock",
                url="https://jobs.seagate.com/search-jobs?keywords=embedded",
                description_snippet="Hard drive firmware for servo control and read channel. "
                "Embedded C, DSP, real-time control loops, motor control.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Networking",
                company="Broadcom",
                location="San Jose, CA",
                source="mock",
                url="https://careers.broadcom.com/jobs?keywords=embedded",
                description_snippet="Embedded firmware for networking ASICs. Linux kernel drivers, "
                "switch/router firmware, C, ARM/MIPS, Memory-mapped I/O.",
            ),
            LeadInput(
                title="Embedded Platform Engineer",
                company="Synaptics",
                location="San Jose, CA",
                source="mock",
                url="https://careers.synaptics.com/jobs?keywords=embedded",
                description_snippet="Firmware for IoT and edge AI platforms. ARM Cortex, "
                "embedded Linux, touch/display controllers, SPI/I2C.",
            ),
            LeadInput(
                title="Embedded Software Engineer - EDA",
                company="Synopsys",
                location="Mountain View, CA",
                source="mock",
                url="https://www.synopsys.com/company/careers/search?keyword=embedded",
                description_snippet="Embedded firmware for IP prototyping platforms. "
                "C/C++, ARM processors, FPGA, hardware emulation.",
            ),
            LeadInput(
                title="Embedded Software Engineer - SoC",
                company="Samsung Semiconductor",
                location="Austin, TX",
                source="mock",
                url="https://semiconductor.samsung.com/us/careers/search?keyword=embedded",
                description_snippet="SoC firmware development. Embedded Linux, ARM TrustZone, "
                "bootloader, power management, C/C++.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Processor IP",
                company="ARM",
                location="Austin, TX",
                source="mock",
                url="https://arm.wd1.myworkdayjobs.com/ARM_Careers/jobs?keywords=embedded",
                description_snippet="Develop embedded software for ARM processor IP validation. "
                "Cortex-M/R/A, RTOS, bare-metal, C/C++, JTAG debugging.",
            ),
            # ── H1B Sponsor Companies - Automotive ──────────────────
            LeadInput(
                title="Embedded Software Engineer - ADAS",
                company="Aptiv",
                location="Troy, MI",
                source="mock",
                url="https://aptiv.avature.net/careers?keyword=embedded",
                description_snippet="ADAS embedded software development. CAN/Ethernet, "
                "AUTOSAR, functional safety, C/C++, sensor fusion, ARM.",
            ),
            LeadInput(
                title="Embedded Controls Engineer - Electric Vehicle",
                company="Ford Motor Company",
                location="Dearborn, MI",
                source="mock",
                url="https://corporate.ford.com/careers/all-jobs.html?keywords=embedded",
                description_snippet="EV powertrain embedded controls. CAN/CAN FD, "
                "MATLAB/Simulink, model-based development, embedded C.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Autonomous Vehicles",
                company="General Motors",
                location="Warren, MI",
                source="mock",
                url="https://search-careers.gm.com/search-jobs?keywords=embedded",
                description_snippet="Autonomous vehicle embedded systems. CAN, Ethernet, "
                "AUTOSAR, Linux, sensor integration, C/C++.",
            ),
            LeadInput(
                title="Embedded Firmware Engineer - Vehicle Controls",
                company="Magna International",
                location="Troy, MI",
                source="mock",
                url="https://careers.magna.com/search?keywords=embedded",
                description_snippet="Vehicle control module firmware. CAN, LIN, "
                "AUTOSAR, embedded C, ISO 26262, powertrain/chassis ECUs.",
            ),
            LeadInput(
                title="Senior Embedded Software Engineer - Powertrain",
                company="Cummins",
                location="Columbus, IN",
                source="mock",
                url="https://jobs.cummins.com/search-jobs?keywords=embedded",
                description_snippet="Diesel/hydrogen engine embedded controls. CAN/J1939, "
                "MATLAB/Simulink, embedded C, RTOS, model-based development.",
            ),
            LeadInput(
                title="Firmware Engineer - Autonomous Driving",
                company="Tesla",
                location="Palo Alto, CA",
                source="mock",
                url="https://www.tesla.com/careers/search?keywords=embedded",
                description_snippet="Autopilot and vehicle firmware. Embedded Linux, C/C++, "
                "CAN, real-time systems, sensor integration, Python testing.",
            ),
            LeadInput(
                title="Embedded Software Engineer - EV Drivetrain",
                company="Lucid Motors",
                location="Newark, CA",
                source="mock",
                url="https://lucidgroup.icims.com/jobs/search?searchKeyword=embedded",
                description_snippet="EV drivetrain embedded software. Motor control, SiC inverters, "
                "CAN/CAN FD, RTOS, embedded C/C++, model-based design.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Transmission",
                company="ZF Group",
                location="Northville, MI",
                source="mock",
                url="https://jobs.zf.com/search-jobs?keywords=embedded",
                description_snippet="Transmission embedded controls. CAN, AUTOSAR, "
                "functional safety, embedded C, ARM MCUs, MATLAB/Simulink.",
            ),
            # ── H1B Sponsor Companies - Aerospace & Defense ─────────
            LeadInput(
                title="Embedded Software Engineer - Avionics",
                company="Boeing",
                location="St. Louis, MO",
                source="mock",
                url="https://jobs.boeing.com/search-jobs?keywords=embedded",
                description_snippet="Avionics embedded software. DO-178C, RTOS, "
                "MIL-STD-1553, ARINC 429, Ada/C/C++, safety-critical systems.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Mission Systems",
                company="Lockheed Martin",
                location="Fort Worth, TX",
                source="mock",
                url="https://jobs.lockheedmartin.com/search-jobs?keywords=embedded",
                description_snippet="Mission-critical embedded systems. DO-178C, RTOS, "
                "C/C++, real-time processing, radar/sensor firmware.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Radar",
                company="Raytheon Technologies",
                location="Tucson, AZ",
                source="mock",
                url="https://www.rtx.com/careers/job-search?keywords=embedded",
                description_snippet="Radar system embedded firmware. FPGA, DSP, "
                "RTOS, C/C++, real-time signal processing, VxWorks.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Defense",
                company="Northrop Grumman",
                location="Baltimore, MD",
                source="mock",
                url="https://www.northropgrumman.com/careers/job-search?searchTerm=embedded",
                description_snippet="Defense embedded systems. C/C++, RTOS, VxWorks, "
                "safety-critical software, DO-178C, MIL-STD.",
            ),
            LeadInput(
                title="Embedded Firmware Engineer - Aviation",
                company="GE Aerospace",
                location="Cincinnati, OH",
                source="mock",
                url="https://jobs.gecareers.com/jobs?keywords=embedded",
                description_snippet="Aviation engine embedded controls. FADEC firmware, "
                "DO-178C, RTOS, model-based development, embedded C.",
            ),
            # ── H1B Sponsor Companies - Robotics & Consumer ─────────
            LeadInput(
                title="Embedded Software Engineer - Robotics",
                company="Boston Dynamics",
                location="Waltham, MA",
                source="mock",
                url="https://jobs.smartrecruiters.com/BostonDynamics?keywords=embedded",
                description_snippet="Robot embedded systems. Motor control, real-time Linux, "
                "C/C++, sensor fusion, CAN, EtherCAT, safety systems.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Robot Firmware",
                company="iRobot",
                location="Bedford, MA",
                source="mock",
                url="https://irobot.taleo.net/careersection/2/jobsearch.ftl?keyword=embedded",
                description_snippet="Consumer robot firmware. ARM Cortex-M, FreeRTOS, "
                "motor control, sensor integration, BLE, Wi-Fi, C.",
            ),
            LeadInput(
                title="Firmware Engineer - Drone Systems",
                company="DJI",
                location="Burlingame, CA",
                source="mock",
                url="https://careers-dji.icims.com/jobs/search?searchKeyword=embedded",
                description_snippet="Drone flight controller firmware. ARM, RTOS, "
                "IMU/GPS sensor fusion, motor ESC control, C/C++.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Imaging",
                company="Sony",
                location="San Jose, CA",
                source="mock",
                url="https://careers.sony.net/job-search?keywords=embedded",
                description_snippet="Camera and imaging sensor embedded firmware. "
                "Image signal processing, ARM, RTOS, C/C++, SPI/MIPI.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Display",
                company="Panasonic",
                location="Newark, NJ",
                source="mock",
                url="https://na.panasonic.com/us/jobs?keywords=embedded",
                description_snippet="Embedded software for industrial displays and infotainment. "
                "Embedded Linux, ARM, CAN, C/C++, display interfaces.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Industrial",
                company="Hitachi",
                location="Santa Clara, CA",
                source="mock",
                url="https://www.hitachi.com/careers/search?keyword=embedded",
                description_snippet="Industrial IoT embedded systems. Embedded Linux, "
                "ARM, sensor networks, MQTT, edge computing, C/C++.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Power",
                company="ABB",
                location="Cary, NC",
                source="mock",
                url="https://careers.abb/global/en/search-results?keywords=embedded",
                description_snippet="Power electronics and robotics embedded firmware. "
                "Motor control, CAN, industrial Ethernet, ARM, RTOS, C/C++.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Telecom",
                company="Ericsson",
                location="Plano, TX",
                source="mock",
                url="https://jobs.ericsson.com/ShowJob/?jldocid=Embedded",
                description_snippet="Telecom base station embedded software. RTOS, Linux, "
                "ARM/DSP, C/C++, real-time networking, 5G RAN firmware.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Networking",
                company="Cisco Systems",
                location="San Jose, CA",
                source="mock",
                url="https://jobs.cisco.com/jobs/Project-Coy-Car_-Enterprise-Embedded-Software-Engineer/1749837",
                description_snippet="Network switch/router embedded software. IOS-XE, Linux, "
                "C, ARM/MIPS, ASIC drivers, protocol stacks.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Networking",
                company="Arista Networks",
                location="Santa Clara, CA",
                source="mock",
                url="https://www.arista.com/en/company/careers?keywords=embedded",
                description_snippet="Network OS embedded development. EOS platform, Linux, "
                "C/C++, switch ASIC firmware, high-performance networking.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Routing",
                company="Juniper Networks",
                location="Sunnyvale, CA",
                source="mock",
                url="https://careers.juniper.net/search-jobs?keywords=embedded",
                description_snippet="Router embedded OS development. Junos, Linux kernel, "
                "C, networking protocols, ASIC integration.",
            ),
            # ── H1B Sponsor Companies - Big Tech (embedded teams) ───
            LeadInput(
                title="Firmware Engineer - Hardware Products",
                company="Apple",
                location="Cupertino, CA",
                source="mock",
                url="https://jobs.apple.com/en/search?keywords=embedded",
                description_snippet="Hardware product firmware. Embedded RTOS, C, "
                "power management, sensor integration, Bluetooth, USB.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Devices",
                company="Google",
                location="Mountain View, CA",
                source="mock",
                url="https://careers.google.com/jobs/results/?q=embedded&location=United%20States",
                description_snippet="Firmware for Pixel, Nest, and hardware products. "
                "Embedded Linux, C/C++, USB, I2C, sensor drivers.",
            ),
            LeadInput(
                title="Firmware Engineer - AR/VR Hardware",
                company="Meta",
                location="Redmond, WA",
                source="mock",
                url="https://www.metacareers.com/jobs?keywords=embedded",
                description_snippet="AR/VR headset firmware. Sensor drivers, RTOS, "
                "C/C++, power management, BLE, USB, display pipelines.",
            ),
            LeadInput(
                title="Firmware Engineer - Surface Devices",
                company="Microsoft",
                location="Redmond, WA",
                source="mock",
                url="https://careers.microsoft.com/us/en/search-results?keywords=embedded",
                description_snippet="Surface hardware firmware. UEFI, embedded controllers, "
                "power management, sensor integration, C/C++.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Devices",
                company="Amazon",
                location="Seattle, WA",
                source="mock",
                url="https://www.amazon.jobs/en/search?keywords=embedded+firmware&location=United%20States",
                description_snippet="Echo/Ring/Kindle device firmware. Embedded Linux, "
                "WiFi/BLE stacks, C/C++, OTA updates, ARM Cortex.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Engines",
                company="Electronic Arts",
                location="Redwood City, CA",
                source="mock",
                url="https://jobs.ea.com/jobs?keywords=embedded",
                description_snippet="Game engine low-level systems. C/C++, memory management, "
                "platform-specific optimizations, GPU programming.",
            ),
            LeadInput(
                title="Embedded Platform Engineer",
                company="Epic Games",
                location="Cary, NC",
                source="mock",
                url="https://www.epicgames.com/site/en-US/careers?keywords=embedded",
                description_snippet="Unreal Engine platform integration. C++, "
                "console hardware, low-level optimization, rendering pipelines.",
            ),
            # ── H1B Sponsor Companies - Cloud/Infra (embedded teams) ──
            LeadInput(
                title="Firmware Engineer - Cloud Hardware",
                company="IBM",
                location="Poughkeepsie, NY",
                source="mock",
                url="https://jobs.ibm.com/search?keywords=embedded",
                description_snippet="Server/mainframe firmware. BMC firmware, "
                "OpenBMC, embedded Linux, C, platform initialization, IPMI.",
            ),
            LeadInput(
                title="Firmware Engineer - Server Platform",
                company="Oracle",
                location="Austin, TX",
                source="mock",
                url="https://oracle.taleo.net/careersection/1/search.ftl?keyword=embedded",
                description_snippet="Server platform firmware. UEFI/BIOS, BMC, "
                "embedded Linux, C, hardware validation, IPMI/Redfish.",
            ),
            LeadInput(
                title="Embedded Software Engineer - Hypervisor",
                company="VMware",
                location="Palo Alto, CA",
                source="mock",
                url="https://careers.vmware.com/jobs?keywords=embedded",
                description_snippet="ESXi embedded platform. Low-level C, device drivers, "
                "hardware abstraction, boot firmware, ARM/x86.",
            ),
            LeadInput(
                title="Embedded Systems Engineer - Linux",
                company="Red Hat",
                location="Raleigh, NC",
                source="mock",
                url="https://jobs.redhat.com/search?keyword=embedded",
                description_snippet="Embedded Linux platform engineering. Kernel, "
                "device drivers, systemd, real-time Linux (PREEMPT_RT), C.",
            ),
            LeadInput(
                title="Firmware Engineer - Telecom Infrastructure",
                company="Lumen Technologies",
                location="Denver, CO",
                source="mock",
                url="https://jobs.lumen.com/jobs?keywords=embedded",
                description_snippet="Telecom network equipment firmware. Embedded Linux, "
                "DPDK, C/C++, network processors, SDN.",
            ),
        ]


class PublicCareersPageAdapter(LeadSource):
    """Adapter for scraping public company career pages.

    TODO: Implement actual web scraping with httpx.
    This adapter would:
    1. Accept a base URL for a public company careers page
    2. Fetch the page via httpx (respecting robots.txt)
    3. Parse job listings (title, location, URL)
    4. Return normalized LeadInput records
    5. Rate limit requests to 1 per 2 seconds

    NOT YET IMPLEMENTED — returns empty list with a warning.
    """

    def __init__(self, company_name: str, careers_url: str) -> None:
        self._company_name = company_name
        self._careers_url = careers_url

    @property
    def source_name(self) -> str:
        return f"careers_page:{self._company_name}"

    def fetch_leads(self, keywords: list[str], location: str | None = None) -> list[LeadInput]:
        # TODO: Implement actual scraping
        # import httpx
        # resp = httpx.get(self._careers_url, follow_redirects=True, timeout=10)
        # ... parse HTML for job listings ...
        return []


class RSSJobSourceAdapter(LeadSource):
    """Adapter for RSS/Atom job feeds.

    TODO: Implement actual RSS feed parsing.
    This adapter would:
    1. Accept an RSS feed URL
    2. Fetch and parse the feed via feedparser or httpx
    3. Extract job titles, companies, URLs
    4. Return normalized LeadInput records

    NOT YET IMPLEMENTED — returns empty list.
    """

    def __init__(self, feed_url: str, source_label: str = "rss") -> None:
        self._feed_url = feed_url
        self._source_label = source_label

    @property
    def source_name(self) -> str:
        return f"rss:{self._source_label}"

    def fetch_leads(self, keywords: list[str], location: str | None = None) -> list[LeadInput]:
        # TODO: Implement actual RSS parsing
        # import httpx
        # resp = httpx.get(self._feed_url, timeout=10)
        # ... parse XML/Atom for job entries ...
        return []




class SerperJobSearchAdapter(LeadSource):
    """Live job search via Serper.dev's Google Jobs API.

    Requires the SERPER_API_KEY environment variable. Returns real, current
    job postings discovered via Google Jobs across LinkedIn, Indeed,
    company sites, and other major boards.
    """

    @property
    def source_name(self) -> str:
        return "serper_google_jobs"

    def fetch_leads(self, keywords: list[str], location: str | None = None) -> list[LeadInput]:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return []

        max_queries = int(os.getenv("SERPER_MAX_QUERIES", "4"))
        results_per_query = int(os.getenv("SERPER_RESULTS_PER_QUERY", "10"))
        gl = os.getenv("SERPER_COUNTRY", "us")

        loc_for_query = (location or "").strip() or "United States"
        queries: list[str] = []
        for kw in keywords[:max_queries]:
            queries.append(f"{kw} {loc_for_query}".strip())

        leads: list[LeadInput] = []
        seen: set[tuple[str, str]] = set()

        for q in queries[:max_queries]:
            try:
                response = httpx.post(
                    "https://google.serper.dev/jobs",
                    headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                    json={"q": q, "gl": gl},
                    timeout=20.0,
                )
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"[SerperJobSearchAdapter] query '{q}' failed: {e}", flush=True)
                continue

            for job in (data.get("jobs") or [])[:results_per_query]:
                title = (job.get("title") or "").strip()
                company = (job.get("company_name") or "").strip()
                if not title or not company:
                    continue
                key = (title.lower(), company.lower())
                if key in seen:
                    continue
                seen.add(key)

                job_loc = (job.get("location") or "").strip() or None
                link = (
                    job.get("link")
                    or job.get("share_link")
                    or job.get("apply_link")
                    or None
                )
                desc_full = job.get("description") or ""
                desc = desc_full[:500] if desc_full else None

                leads.append(
                    LeadInput(
                        title=title,
                        company=company,
                        location=job_loc,
                        source="serper_google_jobs",
                        url=link,
                        description_snippet=desc,
                    )
                )

        return leads


def get_lead_sources() -> list[LeadSource]:
    """Return configured lead sources.

    If SERPER_API_KEY is set, uses the live Serper Google Jobs adapter.
    Otherwise falls back to MockLeadSource so the project still runs end-to-end.
    """
    if os.getenv("SERPER_API_KEY"):
        return [SerperJobSearchAdapter()]
    return [MockLeadSource()]
