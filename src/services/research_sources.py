"""Company research sources.

Provides adapters for gathering public company information.
Currently provides a mock adapter with data for key target companies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.schemas.company import CompanyInput


class ResearchSource(ABC):
    """Abstract base class for company research sources."""

    @abstractmethod
    def research(self, company_name: str) -> CompanyInput | None:
        """Research a company and return structured data. Returns None if not found."""
        ...


class MockResearchSource(ResearchSource):
    """Mock research source with sample company data for target companies."""

    _DATA: dict[str, dict] = {
        # ── Original core companies ─────────────────────────────────
        "CNH Industrial": {
            "name": "CNH Industrial",
            "website": "https://www.cnhindustrial.com",
            "careers_url": "https://careers.cnhindustrial.com/",
            "industry": "Agricultural & Construction Equipment",
            "summary": "Global manufacturer of agricultural and construction equipment, "
            "commercial vehicles, and powertrain solutions. Brands include Case IH, "
            "New Holland, and CASE Construction.",
            "embedded_relevance": "high",
            "research_notes": "Heavy use of embedded controls in sprayers, tractors, and "
            "combines. CAN/J1939 is standard across product lines. Active in precision "
            "agriculture and autonomous vehicle research.",
            "source_url": "https://www.cnhindustrial.com/about-us",
            "suggested_next_step": "apply_now",
        },
        "Deere & Company": {
            "name": "Deere & Company",
            "website": "https://www.deere.com",
            "careers_url": "https://jobs.deere.com/search-jobs?keywords=embedded",
            "industry": "Agricultural & Construction Equipment",
            "summary": "World's largest manufacturer of agricultural equipment. "
            "Also produces construction, forestry, and diesel engines.",
            "embedded_relevance": "high",
            "research_notes": "Major embedded software employer. Uses CAN/J1939 extensively. "
            "Investing heavily in autonomy, precision ag, and edge computing.",
            "source_url": "https://www.deere.com/en/our-company/",
            "suggested_next_step": "apply_now",
        },
        "Rockwell Automation": {
            "name": "Rockwell Automation",
            "website": "https://www.rockwellautomation.com",
            "careers_url": "https://www.rockwellautomation.com/en-us/company/careers.html",
            "industry": "Industrial Automation",
            "summary": "Global leader in industrial automation and digital transformation. "
            "Products include PLCs, drives, and industrial IoT platforms.",
            "embedded_relevance": "high",
            "research_notes": "Firmware roles for industrial controllers. "
            "Uses FreeRTOS, embedded Linux, and industrial Ethernet protocols.",
            "source_url": "https://www.rockwellautomation.com/about-us",
            "suggested_next_step": "apply_now",
        },
        "Oshkosh Corporation": {
            "name": "Oshkosh Corporation",
            "website": "https://www.oshkoshcorp.com",
            "careers_url": "https://oshkoshcorporation.jobs/",
            "industry": "Specialty Vehicles",
            "summary": "Manufacturer of specialty vehicles including fire trucks, "
            "military vehicles, and access equipment.",
            "embedded_relevance": "high",
            "research_notes": "Vehicle control systems, CAN bus, embedded software "
            "for defense and commercial vehicles.",
            "source_url": "https://www.oshkoshcorp.com/about",
            "suggested_next_step": "apply_now",
        },
        "Bosch": {
            "name": "Bosch",
            "website": "https://www.bosch.com",
            "careers_url": "https://www.bosch.us/careers/search/?keywords=embedded",
            "industry": "Automotive & Industrial Technology",
            "summary": "Global supplier of automotive and industrial technology, consumer goods, "
            "and building technology. Major automotive Tier 1 supplier.",
            "embedded_relevance": "high",
            "research_notes": "Massive embedded software org — AUTOSAR, powertrain ECUs, "
            "ADAS, industrial IoT. Heavy C/C++, CAN, functional safety (ISO 26262). "
            "Offices in Plymouth, MI and other US locations.",
            "source_url": "https://www.bosch.com/company/",
            "suggested_next_step": "apply_now",
        },
        "Continental": {
            "name": "Continental",
            "website": "https://www.continental.com",
            "careers_url": "https://jobs-continental.icims.com/jobs/search?searchKeyword=embedded",
            "industry": "Automotive Technology",
            "summary": "Global automotive supplier specializing in tires, brake systems, "
            "powertrain, chassis, and vehicle electronics.",
            "embedded_relevance": "high",
            "research_notes": "Vehicle electronics firmware, ARM Cortex MCUs, CAN/LIN/FlexRay, "
            "AUTOSAR, functional safety. Strong embedded teams in Auburn Hills, MI.",
            "source_url": "https://www.continental.com/en/company/",
            "suggested_next_step": "engage_employees",
        },
        "AGCO Corporation": {
            "name": "AGCO Corporation",
            "website": "https://www.agcocorp.com",
            "careers_url": "https://careers.agcocorp.com/",
            "industry": "Agricultural Equipment",
            "summary": "Global manufacturer of agricultural equipment under brands "
            "Fendt, Massey Ferguson, Valtra, and GSI.",
            "embedded_relevance": "high",
            "research_notes": "Controls software for tractors, sprayers, combines. "
            "Uses MATLAB/Simulink, J1939, embedded C. Precision agriculture focus. "
            "Locations in Hesston KS, Jackson MN.",
            "source_url": "https://www.agcocorp.com/company.html",
            "suggested_next_step": "apply_now",
        },
        "Caterpillar": {
            "name": "Caterpillar",
            "website": "https://www.caterpillar.com",
            "careers_url": "https://www.caterpillar.com/en/careers.html",
            "industry": "Construction & Mining Equipment",
            "summary": "World's leading manufacturer of construction and mining equipment, "
            "diesel and natural gas engines, industrial gas turbines.",
            "embedded_relevance": "high",
            "research_notes": "Embedded controls for dozers, excavators, mining trucks. "
            "CAN/J1939, STM32, RTOS, model-based development. "
            "Investing in autonomous mining and remote operation.",
            "source_url": "https://www.caterpillar.com/en/company.html",
            "suggested_next_step": "apply_now",
        },
        "Siemens": {
            "name": "Siemens",
            "website": "https://www.siemens.com",
            "careers_url": "https://jobs.siemens.com/",
            "industry": "Industrial Automation & Digitalization",
            "summary": "Global technology company focused on industry, infrastructure, "
            "transport, and healthcare. Major PLC and industrial automation provider.",
            "embedded_relevance": "medium",
            "research_notes": "Industrial automation controllers, SCADA systems, embedded Linux. "
            "More PLC/HMI focused than bare-metal embedded. Strong in industrial IoT. "
            "Relevant for controls-adjacent roles.",
            "source_url": "https://www.siemens.com/global/en/company/about.html",
            "suggested_next_step": "monitor_weekly",
        },
        "Parker Hannifin": {
            "name": "Parker Hannifin",
            "website": "https://www.parker.com",
            "careers_url": "https://www.parker.com/careers",
            "industry": "Motion & Control Technologies",
            "summary": "Global leader in motion and control technologies. "
            "Products include hydraulic, pneumatic, and electromechanical systems.",
            "embedded_relevance": "high",
            "research_notes": "Firmware for hydraulic and electromechanical controllers. "
            "FreeRTOS, CAN bus, safety-critical systems. "
            "Strong embedded roles in Cleveland, OH area.",
            "source_url": "https://www.parker.com/about",
            "suggested_next_step": "apply_now",
        },
        "Honeywell": {
            "name": "Honeywell",
            "website": "https://www.honeywell.com",
            "careers_url": "https://careers.honeywell.com/jobs?keywords=embedded",
            "industry": "Aerospace & Industrial",
            "summary": "Diversified technology company with aerospace, building technologies, "
            "and performance materials divisions.",
            "embedded_relevance": "high",
            "research_notes": "IoT edge devices, aerospace firmware, building automation. "
            "Remote-friendly positions available. Uses embedded Linux, BLE, sensor fusion.",
            "source_url": "https://www.honeywell.com/us/en/company/about-us",
            "suggested_next_step": "apply_now",
        },
        "Medtronic": {
            "name": "Medtronic",
            "website": "https://www.medtronic.com",
            "careers_url": "https://jobs.medtronic.com/",
            "industry": "Medical Devices",
            "summary": "World's largest medical device company. Products include "
            "cardiac devices, surgical instruments, and diabetes management systems.",
            "embedded_relevance": "medium",
            "research_notes": "Safety-critical embedded software for medical devices. "
            "C/C++, RTOS, IEC 62304 compliance. Different domain but transferable skills. "
            "Minneapolis, MN area.",
            "source_url": "https://www.medtronic.com/us-en/about.html",
            "suggested_next_step": "follow_company",
        },
        # ── H1B Sponsor Companies - Semiconductor / Chip ────────────
        "Qualcomm": {
            "name": "Qualcomm",
            "website": "https://www.qualcomm.com",
            "careers_url": "https://jobs.qualcomm.com/search-jobs?keywords=embedded",
            "industry": "Semiconductor - Wireless",
            "summary": "Leading designer of wireless SoCs for mobile, IoT, and automotive. "
            "Snapdragon processor family.",
            "embedded_relevance": "high",
            "research_notes": "Massive embedded firmware org. ARM Cortex-M/A, Wi-Fi/BT stacks, "
            "cellular modem firmware, RTOS, low-power design. H1B sponsor.",
            "source_url": "https://www.qualcomm.com/company/about",
            "suggested_next_step": "apply_now",
        },
        "Intel": {
            "name": "Intel",
            "website": "https://www.intel.com",
            "careers_url": "https://jobs.intel.com/Search/Results?keyword=embedded",
            "industry": "Semiconductor - Processors",
            "summary": "World's largest semiconductor chip maker. x86 processors, FPGAs (Altera), "
            "and embedded solutions.",
            "embedded_relevance": "high",
            "research_notes": "SoC firmware, BIOS/UEFI, embedded Linux BSP, FPGA tools. "
            "Large firmware teams in OR, AZ, CA. H1B sponsor.",
            "source_url": "https://www.intel.com/content/www/us/en/company-overview/company-overview.html",
            "suggested_next_step": "apply_now",
        },
        "Texas Instruments": {
            "name": "Texas Instruments",
            "website": "https://www.ti.com",
            "careers_url": "https://careers.ti.com/jobs?keywords=embedded",
            "industry": "Semiconductor - Analog & MCU",
            "summary": "Leading analog and embedded processor company. "
            "MSP430, C2000, Sitara, and AM6x MCU/MPU families.",
            "embedded_relevance": "high",
            "research_notes": "SDK/firmware teams for TI MCUs. Bare-metal, TI-RTOS, "
            "CAN/SPI/I2C drivers. Core embedded employer. Dallas, TX. H1B sponsor.",
            "source_url": "https://www.ti.com/about-ti/company/ti-at-a-glance.html",
            "suggested_next_step": "apply_now",
        },
        "Analog Devices": {
            "name": "Analog Devices",
            "website": "https://www.analog.com",
            "careers_url": "https://www.analog.com/en/about-adi/careers?keywords=embedded",
            "industry": "Semiconductor - Analog & Mixed Signal",
            "summary": "High-performance analog, mixed-signal, and DSP integrated circuits.",
            "embedded_relevance": "high",
            "research_notes": "Embedded firmware for precision sensors, data converters, "
            "and signal conditioning ICs. SPI/I2C, DSP, low-power. H1B sponsor.",
            "source_url": "https://www.analog.com/en/about-adi.html",
            "suggested_next_step": "apply_now",
        },
        "Infineon": {
            "name": "Infineon",
            "website": "https://www.infineon.com",
            "careers_url": "https://infineon.wd3.myworkdayjobs.com/infineonexternal?keywords=embedded",
            "industry": "Semiconductor - Automotive & Power",
            "summary": "Major automotive MCU and power semiconductor company. "
            "AURIX, PSoC, and XMC MCU families.",
            "embedded_relevance": "high",
            "research_notes": "Automotive MCU firmware, AUTOSAR MCAL, CAN/LIN, "
            "functional safety. Very relevant to automotive embedded background. H1B sponsor.",
            "source_url": "https://www.infineon.com/cms/en/about-infineon/",
            "suggested_next_step": "apply_now",
        },
        "Micron Technology": {
            "name": "Micron Technology",
            "website": "https://www.micron.com",
            "careers_url": "https://jobs.micron.com/search?keyword=embedded",
            "industry": "Semiconductor - Memory",
            "summary": "Major DRAM and NAND flash memory manufacturer.",
            "embedded_relevance": "medium",
            "research_notes": "Firmware for memory controllers. Embedded C/C++, "
            "RTOS, DMA, performance optimization. Boise, ID. H1B sponsor.",
            "source_url": "https://www.micron.com/about",
            "suggested_next_step": "follow_company",
        },
        "Western Digital": {
            "name": "Western Digital",
            "website": "https://www.westerndigital.com",
            "careers_url": "https://jobs.westerndigital.com/search-jobs?keywords=embedded",
            "industry": "Data Storage",
            "summary": "Major data storage company. WD, SanDisk, and HGST brands.",
            "embedded_relevance": "medium",
            "research_notes": "SSD/HDD controller firmware. C/C++, RTOS, NVMe, "
            "ARM platforms. Milpitas, CA. H1B sponsor.",
            "source_url": "https://www.westerndigital.com/company",
            "suggested_next_step": "follow_company",
        },
        "Seagate Technology": {
            "name": "Seagate Technology",
            "website": "https://www.seagate.com",
            "careers_url": "https://jobs.seagate.com/search-jobs?keywords=embedded",
            "industry": "Data Storage",
            "summary": "Major hard drive and storage solutions manufacturer.",
            "embedded_relevance": "medium",
            "research_notes": "HDD firmware: servo control, read channel, motor control. "
            "Embedded C, DSP. Shakopee, MN. H1B sponsor.",
            "source_url": "https://www.seagate.com/our-story/",
            "suggested_next_step": "follow_company",
        },
        "Broadcom": {
            "name": "Broadcom",
            "website": "https://www.broadcom.com",
            "careers_url": "https://careers.broadcom.com/jobs?keywords=embedded",
            "industry": "Semiconductor - Networking",
            "summary": "Major networking and broadband semiconductor company. "
            "Also owns VMware, Symantec, and CA Technologies.",
            "embedded_relevance": "high",
            "research_notes": "Networking ASIC firmware, Linux kernel drivers, "
            "switch/router firmware. C, ARM/MIPS. San Jose, CA. H1B sponsor.",
            "source_url": "https://www.broadcom.com/company/about-us",
            "suggested_next_step": "apply_now",
        },
        "Synaptics": {
            "name": "Synaptics",
            "website": "https://www.synaptics.com",
            "careers_url": "https://careers.synaptics.com/jobs?keywords=embedded",
            "industry": "Semiconductor - IoT & HMI",
            "summary": "IoT and human machine interface semiconductor company. "
            "Touch controllers, display drivers, edge AI.",
            "embedded_relevance": "high",
            "research_notes": "Firmware for IoT and edge AI platforms. "
            "ARM Cortex, touch/display, SPI/I2C. San Jose, CA. H1B sponsor.",
            "source_url": "https://www.synaptics.com/company",
            "suggested_next_step": "follow_company",
        },
        "Synopsys": {
            "name": "Synopsys",
            "website": "https://www.synopsys.com",
            "careers_url": "https://www.synopsys.com/company/careers/search?keyword=embedded",
            "industry": "EDA & IP",
            "summary": "Leading EDA tools and semiconductor IP provider.",
            "embedded_relevance": "medium",
            "research_notes": "Embedded firmware for IP prototyping platforms. "
            "C/C++, ARM, FPGA, hardware emulation. Mountain View, CA. H1B sponsor.",
            "source_url": "https://www.synopsys.com/company.html",
            "suggested_next_step": "follow_company",
        },
        "Samsung Semiconductor": {
            "name": "Samsung Semiconductor",
            "website": "https://semiconductor.samsung.com",
            "careers_url": "https://semiconductor.samsung.com/us/careers/search?keyword=embedded",
            "industry": "Semiconductor - Memory & SoC",
            "summary": "Samsung's semiconductor division. Exynos SoCs, DRAM, NAND.",
            "embedded_relevance": "high",
            "research_notes": "SoC firmware, embedded Linux, ARM TrustZone, bootloaders. "
            "Austin, TX and San Jose, CA offices. H1B sponsor.",
            "source_url": "https://semiconductor.samsung.com/us/about-us/",
            "suggested_next_step": "apply_now",
        },
        "ARM": {
            "name": "ARM",
            "website": "https://www.arm.com",
            "careers_url": "https://arm.wd1.myworkdayjobs.com/ARM_Careers/jobs?keywords=embedded",
            "industry": "Semiconductor - Processor IP",
            "summary": "Designer of ARM processor architecture used in billions of devices.",
            "embedded_relevance": "high",
            "research_notes": "Embedded SW for processor IP validation. Cortex-M/R/A, "
            "RTOS, bare-metal C/C++, JTAG. Austin, TX and San Jose, CA. H1B sponsor.",
            "source_url": "https://www.arm.com/company",
            "suggested_next_step": "apply_now",
        },
        # ── H1B Sponsor Companies - Automotive ──────────────────────
        "Aptiv": {
            "name": "Aptiv",
            "website": "https://www.aptiv.com",
            "careers_url": "https://aptiv.avature.net/careers?keyword=embedded",
            "industry": "Automotive - ADAS & Connectivity",
            "summary": "Global technology company focused on vehicle safety, "
            "advanced driver-assistance systems, and autonomous driving.",
            "embedded_relevance": "high",
            "research_notes": "ADAS embedded software, CAN/Ethernet, AUTOSAR, "
            "functional safety, sensor fusion. Troy, MI. H1B sponsor.",
            "source_url": "https://www.aptiv.com/about",
            "suggested_next_step": "apply_now",
        },
        "Ford Motor Company": {
            "name": "Ford Motor Company",
            "website": "https://www.ford.com",
            "careers_url": "https://corporate.ford.com/careers/all-jobs.html?keywords=embedded",
            "industry": "Automotive OEM",
            "summary": "American multinational automaker. Major EV push with F-150 Lightning, "
            "Mustang Mach-E, and commercial EVs.",
            "embedded_relevance": "high",
            "research_notes": "EV powertrain controls, CAN/CAN FD, MATLAB/Simulink, "
            "model-based development. Dearborn, MI. H1B sponsor.",
            "source_url": "https://corporate.ford.com/about.html",
            "suggested_next_step": "apply_now",
        },
        "General Motors": {
            "name": "General Motors",
            "website": "https://www.gm.com",
            "careers_url": "https://search-careers.gm.com/search-jobs?keywords=embedded",
            "industry": "Automotive OEM",
            "summary": "Major American automaker. Ultium EV platform, Cruise autonomous vehicles.",
            "embedded_relevance": "high",
            "research_notes": "Autonomous vehicle embedded systems, CAN, Ethernet, "
            "AUTOSAR, Linux. Warren, MI. H1B sponsor.",
            "source_url": "https://www.gm.com/company/about-gm",
            "suggested_next_step": "apply_now",
        },
        "Magna International": {
            "name": "Magna International",
            "website": "https://www.magna.com",
            "careers_url": "https://careers.magna.com/search?keywords=embedded",
            "industry": "Automotive Tier 1 Supplier",
            "summary": "One of the world's largest automotive suppliers. "
            "Vehicle engineering, electronics, and complete vehicle assembly.",
            "embedded_relevance": "high",
            "research_notes": "Vehicle control module firmware, CAN, LIN, AUTOSAR, "
            "embedded C, ISO 26262. Troy, MI. H1B sponsor.",
            "source_url": "https://www.magna.com/company",
            "suggested_next_step": "apply_now",
        },
        "Cummins": {
            "name": "Cummins",
            "website": "https://www.cummins.com",
            "careers_url": "https://jobs.cummins.com/search-jobs?keywords=embedded",
            "industry": "Engines & Power Generation",
            "summary": "Global power solutions company. Diesel, natural gas, electric, "
            "and hydrogen powertrains.",
            "embedded_relevance": "high",
            "research_notes": "Engine embedded controls, CAN/J1939, MATLAB/Simulink, "
            "model-based development. Columbus, IN. H1B sponsor.",
            "source_url": "https://www.cummins.com/company",
            "suggested_next_step": "apply_now",
        },
        "Tesla": {
            "name": "Tesla",
            "website": "https://www.tesla.com",
            "careers_url": "https://www.tesla.com/careers/search?keywords=embedded",
            "industry": "Automotive - EV & Energy",
            "summary": "Electric vehicle and clean energy company. "
            "Autopilot, FSD, Megapack, Solar.",
            "embedded_relevance": "high",
            "research_notes": "Autopilot firmware, vehicle ECU software, embedded Linux, "
            "C/C++, CAN, real-time systems. Palo Alto, CA. H1B sponsor.",
            "source_url": "https://www.tesla.com/about",
            "suggested_next_step": "apply_now",
        },
        "Lucid Motors": {
            "name": "Lucid Motors",
            "website": "https://www.lucidmotors.com",
            "careers_url": "https://lucidgroup.icims.com/jobs/search?searchKeyword=embedded",
            "industry": "Automotive - EV",
            "summary": "Luxury EV maker. Lucid Air sedan and Gravity SUV.",
            "embedded_relevance": "high",
            "research_notes": "EV drivetrain firmware, motor control, CAN/CAN FD, "
            "RTOS, model-based design. Newark, CA. H1B sponsor.",
            "source_url": "https://www.lucidmotors.com/company",
            "suggested_next_step": "apply_now",
        },
        "ZF Group": {
            "name": "ZF Group",
            "website": "https://www.zf.com",
            "careers_url": "https://jobs.zf.com/search-jobs?keywords=embedded",
            "industry": "Automotive - Drivetrain & Safety",
            "summary": "Major automotive supplier. Transmissions, steering, chassis, "
            "and safety systems.",
            "embedded_relevance": "high",
            "research_notes": "Transmission embedded controls, CAN, AUTOSAR, "
            "functional safety, MATLAB/Simulink. Northville, MI. H1B sponsor.",
            "source_url": "https://www.zf.com/mobile/en/company/company.html",
            "suggested_next_step": "apply_now",
        },
        # ── H1B Sponsor Companies - Aerospace & Defense ─────────────
        "Boeing": {
            "name": "Boeing",
            "website": "https://www.boeing.com",
            "careers_url": "https://jobs.boeing.com/search-jobs?keywords=embedded",
            "industry": "Aerospace & Defense",
            "summary": "World's largest aerospace company. Commercial aircraft, "
            "defense, and space systems.",
            "embedded_relevance": "high",
            "research_notes": "Avionics firmware, DO-178C, RTOS, MIL-STD-1553, "
            "ARINC 429, Ada/C/C++. St. Louis, MO and Seattle, WA. H1B sponsor.",
            "source_url": "https://www.boeing.com/company/",
            "suggested_next_step": "apply_now",
        },
        "Lockheed Martin": {
            "name": "Lockheed Martin",
            "website": "https://www.lockheedmartin.com",
            "careers_url": "https://jobs.lockheedmartin.com/search-jobs?keywords=embedded",
            "industry": "Aerospace & Defense",
            "summary": "Largest defense contractor globally. F-35, missiles, satellites, "
            "and cyber security.",
            "embedded_relevance": "high",
            "research_notes": "Mission-critical embedded systems, DO-178C, RTOS, "
            "C/C++, radar/sensor firmware. Fort Worth, TX. H1B sponsor.",
            "source_url": "https://www.lockheedmartin.com/en-us/who-we-are.html",
            "suggested_next_step": "apply_now",
        },
        "Raytheon Technologies": {
            "name": "Raytheon Technologies",
            "website": "https://www.rtx.com",
            "careers_url": "https://www.rtx.com/careers/job-search?keywords=embedded",
            "industry": "Aerospace & Defense",
            "summary": "Major defense and aerospace company (RTX). Pratt & Whitney engines, "
            "Collins Aerospace, Raytheon missiles.",
            "embedded_relevance": "high",
            "research_notes": "Radar firmware, FPGA, DSP, RTOS, VxWorks, C/C++. "
            "Tucson, AZ and multiple US locations. H1B sponsor.",
            "source_url": "https://www.rtx.com/who-we-are",
            "suggested_next_step": "apply_now",
        },
        "Northrop Grumman": {
            "name": "Northrop Grumman",
            "website": "https://www.northropgrumman.com",
            "careers_url": "https://www.northropgrumman.com/careers/job-search?searchTerm=embedded",
            "industry": "Aerospace & Defense",
            "summary": "Major defense contractor. B-21 bomber, space systems, "
            "autonomous systems, and cyber.",
            "embedded_relevance": "high",
            "research_notes": "Defense embedded systems, RTOS, VxWorks, DO-178C, "
            "safety-critical C/C++. Baltimore, MD. H1B sponsor.",
            "source_url": "https://www.northropgrumman.com/who-we-are",
            "suggested_next_step": "apply_now",
        },
        "GE Aerospace": {
            "name": "GE Aerospace",
            "website": "https://www.geaerospace.com",
            "careers_url": "https://jobs.gecareers.com/jobs?keywords=embedded",
            "industry": "Aerospace - Engines",
            "summary": "Leading jet engine manufacturer. LEAP and GE9X engines.",
            "embedded_relevance": "high",
            "research_notes": "FADEC engine control firmware, DO-178C, RTOS, "
            "model-based development. Cincinnati, OH. H1B sponsor.",
            "source_url": "https://www.geaerospace.com/company",
            "suggested_next_step": "apply_now",
        },
        # ── H1B Sponsor Companies - Robotics / Consumer HW ─────────
        "Boston Dynamics": {
            "name": "Boston Dynamics",
            "website": "https://www.bostondynamics.com",
            "careers_url": "https://jobs.smartrecruiters.com/BostonDynamics?keywords=embedded",
            "industry": "Robotics",
            "summary": "Advanced robotics company. Spot, Stretch, and Atlas robots.",
            "embedded_relevance": "high",
            "research_notes": "Robot embedded systems, motor control, real-time Linux, "
            "CAN, EtherCAT, sensor fusion. Waltham, MA. H1B sponsor.",
            "source_url": "https://www.bostondynamics.com/about",
            "suggested_next_step": "apply_now",
        },
        "iRobot": {
            "name": "iRobot",
            "website": "https://www.irobot.com",
            "careers_url": "https://irobot.taleo.net/careersection/2/jobsearch.ftl?keyword=embedded",
            "industry": "Consumer Robotics",
            "summary": "Consumer robot company. Roomba vacuums and home robots.",
            "embedded_relevance": "high",
            "research_notes": "Consumer robot firmware, ARM Cortex-M, FreeRTOS, "
            "motor control, BLE, Wi-Fi. Bedford, MA. H1B sponsor.",
            "source_url": "https://www.irobot.com/about-irobot",
            "suggested_next_step": "follow_company",
        },
        "DJI": {
            "name": "DJI",
            "website": "https://www.dji.com",
            "careers_url": "https://careers-dji.icims.com/jobs/search?searchKeyword=embedded",
            "industry": "Drones & Imaging",
            "summary": "World's largest consumer drone manufacturer. "
            "Also gimbal cameras and action cameras.",
            "embedded_relevance": "high",
            "research_notes": "Drone flight controller firmware, ARM, RTOS, "
            "IMU/GPS sensor fusion, motor ESC. Burlingame, CA. H1B sponsor.",
            "source_url": "https://www.dji.com/company",
            "suggested_next_step": "apply_now",
        },
        "Sony": {
            "name": "Sony",
            "website": "https://www.sony.com",
            "careers_url": "https://careers.sony.net/job-search?keywords=embedded",
            "industry": "Consumer Electronics & Imaging",
            "summary": "Global electronics and entertainment conglomerate. "
            "PlayStation, cameras, image sensors.",
            "embedded_relevance": "medium",
            "research_notes": "Camera/imaging sensor firmware, image signal processing, "
            "ARM, RTOS, SPI/MIPI. San Jose, CA. H1B sponsor.",
            "source_url": "https://www.sony.com/en/SonyInfo/CorporateInfo/",
            "suggested_next_step": "follow_company",
        },
        "Panasonic": {
            "name": "Panasonic",
            "website": "https://www.panasonic.com",
            "careers_url": "https://na.panasonic.com/us/jobs?keywords=embedded",
            "industry": "Electronics & Industrial",
            "summary": "Japanese multinational electronics. Automotive batteries, "
            "avionics displays, industrial solutions.",
            "embedded_relevance": "medium",
            "research_notes": "Embedded software for displays, infotainment, automotive. "
            "Embedded Linux, ARM, CAN. Newark, NJ. H1B sponsor.",
            "source_url": "https://www.panasonic.com/global/corporate/about.html",
            "suggested_next_step": "follow_company",
        },
        "Hitachi": {
            "name": "Hitachi",
            "website": "https://www.hitachi.com",
            "careers_url": "https://www.hitachi.com/careers/search?keyword=embedded",
            "industry": "Industrial & IT",
            "summary": "Japanese conglomerate. Industrial equipment, IT services, "
            "energy systems.",
            "embedded_relevance": "medium",
            "research_notes": "Industrial IoT embedded systems, embedded Linux, "
            "sensor networks, edge computing. Santa Clara, CA. H1B sponsor.",
            "source_url": "https://www.hitachi.com/corporate/about/",
            "suggested_next_step": "follow_company",
        },
        "ABB": {
            "name": "ABB",
            "website": "https://www.abb.com",
            "careers_url": "https://careers.abb/global/en/search-results?keywords=embedded",
            "industry": "Industrial Automation & Robotics",
            "summary": "Global technology company in electrification, automation, "
            "motion, and robotics.",
            "embedded_relevance": "high",
            "research_notes": "Power electronics and robotics firmware, motor control, "
            "CAN, industrial Ethernet, ARM, RTOS. Cary, NC. H1B sponsor.",
            "source_url": "https://global.abb/group/en/about",
            "suggested_next_step": "apply_now",
        },
        "Ericsson": {
            "name": "Ericsson",
            "website": "https://www.ericsson.com",
            "careers_url": "https://jobs.ericsson.com/ShowJob/?jldocid=Embedded",
            "industry": "Telecom Equipment",
            "summary": "Global telecom equipment and 5G infrastructure provider.",
            "embedded_relevance": "medium",
            "research_notes": "Base station embedded software, RTOS, Linux, "
            "ARM/DSP, 5G RAN firmware. Plano, TX. H1B sponsor.",
            "source_url": "https://www.ericsson.com/en/about-us",
            "suggested_next_step": "follow_company",
        },
        # ── H1B Sponsor Companies - Networking ──────────────────────
        "Cisco Systems": {
            "name": "Cisco Systems",
            "website": "https://www.cisco.com",
            "careers_url": "https://jobs.cisco.com/jobs/Project-Coy-Car_-Enterprise-Embedded-Software-Engineer/1749837",
            "industry": "Networking & Security",
            "summary": "World's largest networking equipment company. "
            "Routers, switches, security, collaboration.",
            "embedded_relevance": "high",
            "research_notes": "Network switch/router embedded OS (IOS-XE), Linux, "
            "C, ASIC drivers. San Jose, CA. H1B sponsor.",
            "source_url": "https://www.cisco.com/c/en/us/about/company-information.html",
            "suggested_next_step": "apply_now",
        },
        "Arista Networks": {
            "name": "Arista Networks",
            "website": "https://www.arista.com",
            "careers_url": "https://www.arista.com/en/company/careers?keywords=embedded",
            "industry": "Networking",
            "summary": "Cloud networking company. High-performance data center switches.",
            "embedded_relevance": "high",
            "research_notes": "Network OS embedded development (EOS), Linux, C/C++, "
            "switch ASIC firmware. Santa Clara, CA. H1B sponsor.",
            "source_url": "https://www.arista.com/en/company/about-us",
            "suggested_next_step": "apply_now",
        },
        "Juniper Networks": {
            "name": "Juniper Networks",
            "website": "https://www.juniper.net",
            "careers_url": "https://careers.juniper.net/search-jobs?keywords=embedded",
            "industry": "Networking",
            "summary": "Networking and cybersecurity company. Junos OS routers and switches.",
            "embedded_relevance": "high",
            "research_notes": "Router embedded OS (Junos), Linux kernel, C, "
            "networking protocols. Sunnyvale, CA. H1B sponsor.",
            "source_url": "https://www.juniper.net/us/en/company/",
            "suggested_next_step": "follow_company",
        },
        # ── H1B Sponsor Companies - Big Tech ────────────────────────
        "Apple": {
            "name": "Apple",
            "website": "https://www.apple.com",
            "careers_url": "https://jobs.apple.com/en/search?keywords=embedded",
            "industry": "Consumer Electronics & Software",
            "summary": "World's most valuable company. iPhone, Mac, Apple Watch, AirPods.",
            "embedded_relevance": "high",
            "research_notes": "Hardware product firmware, RTOS, C, power management, "
            "sensor integration, Bluetooth, USB. Cupertino, CA. H1B sponsor.",
            "source_url": "https://www.apple.com/leadership/",
            "suggested_next_step": "apply_now",
        },
        "Google": {
            "name": "Google",
            "website": "https://www.google.com",
            "careers_url": "https://careers.google.com/jobs/results/?q=embedded&location=United%20States",
            "industry": "Technology",
            "summary": "Global technology leader. Search, cloud, Android, Pixel, Nest, "
            "and Waymo autonomous vehicles.",
            "embedded_relevance": "medium",
            "research_notes": "Firmware for Pixel, Nest, and Chromebook hardware. "
            "Embedded Linux, C/C++, sensor drivers. Mountain View, CA. H1B sponsor.",
            "source_url": "https://about.google/",
            "suggested_next_step": "follow_company",
        },
        "Meta": {
            "name": "Meta",
            "website": "https://www.meta.com",
            "careers_url": "https://www.metacareers.com/jobs?keywords=embedded",
            "industry": "Technology - Social & AR/VR",
            "summary": "Social media and AR/VR technology company. "
            "Quest VR headsets, Ray-Ban Meta glasses.",
            "embedded_relevance": "medium",
            "research_notes": "AR/VR headset firmware, sensor drivers, RTOS, "
            "power management, BLE, USB. Redmond, WA. H1B sponsor.",
            "source_url": "https://about.meta.com/",
            "suggested_next_step": "follow_company",
        },
        "Microsoft": {
            "name": "Microsoft",
            "website": "https://www.microsoft.com",
            "careers_url": "https://careers.microsoft.com/us/en/search-results?keywords=embedded",
            "industry": "Technology - Cloud & Hardware",
            "summary": "Global technology company. Azure, Windows, Office, Surface, Xbox, HoloLens.",
            "embedded_relevance": "medium",
            "research_notes": "Surface device firmware, UEFI, embedded controllers, "
            "HoloLens firmware. Redmond, WA. H1B sponsor.",
            "source_url": "https://www.microsoft.com/en-us/about",
            "suggested_next_step": "follow_company",
        },
        "Amazon": {
            "name": "Amazon",
            "website": "https://www.amazon.com",
            "careers_url": "https://www.amazon.jobs/en/search?keywords=embedded+firmware&location=United%20States",
            "industry": "Technology - E-commerce & Cloud",
            "summary": "World's largest e-commerce and cloud company (AWS). "
            "Also Echo, Ring, Kindle, and Kuiper satellite.",
            "embedded_relevance": "medium",
            "research_notes": "Echo/Ring/Kindle device firmware. Embedded Linux, "
            "WiFi/BLE, C/C++, OTA updates, ARM. Seattle, WA. H1B sponsor.",
            "source_url": "https://www.aboutamazon.com/",
            "suggested_next_step": "follow_company",
        },
        # ── H1B Sponsor Companies - Cloud / Infra (embedded) ───────
        "IBM": {
            "name": "IBM",
            "website": "https://www.ibm.com",
            "careers_url": "https://jobs.ibm.com/search?keywords=embedded",
            "industry": "Technology - Cloud & Enterprise",
            "summary": "Global technology and consulting multinational. "
            "Mainframes, cloud, AI, and quantum computing.",
            "embedded_relevance": "medium",
            "research_notes": "Server/mainframe firmware, BMC firmware, OpenBMC, "
            "embedded Linux, IPMI. Poughkeepsie, NY. H1B sponsor.",
            "source_url": "https://www.ibm.com/about",
            "suggested_next_step": "follow_company",
        },
        "Oracle": {
            "name": "Oracle",
            "website": "https://www.oracle.com",
            "careers_url": "https://oracle.taleo.net/careersection/1/search.ftl?keyword=embedded",
            "industry": "Technology - Database & Cloud",
            "summary": "Enterprise software and cloud infrastructure company.",
            "embedded_relevance": "low",
            "research_notes": "Server platform firmware, UEFI/BIOS, BMC. "
            "Limited embedded roles vs. software. Austin, TX. H1B sponsor.",
            "source_url": "https://www.oracle.com/corporate/",
            "suggested_next_step": "monitor_weekly",
        },
        "VMware": {
            "name": "VMware",
            "website": "https://www.vmware.com",
            "careers_url": "https://careers.vmware.com/jobs?keywords=embedded",
            "industry": "Virtualization & Cloud",
            "summary": "Virtualization and cloud infrastructure company (now Broadcom).",
            "embedded_relevance": "low",
            "research_notes": "ESXi embedded platform, device drivers, hardware abstraction. "
            "Palo Alto, CA. H1B sponsor.",
            "source_url": "https://www.vmware.com/company.html",
            "suggested_next_step": "monitor_weekly",
        },
        "Red Hat": {
            "name": "Red Hat",
            "website": "https://www.redhat.com",
            "careers_url": "https://jobs.redhat.com/search?keyword=embedded",
            "industry": "Open Source Software",
            "summary": "Leading enterprise open-source software company (IBM subsidiary). RHEL, OpenShift.",
            "embedded_relevance": "medium",
            "research_notes": "Embedded Linux platform engineering, kernel, device drivers, "
            "real-time Linux (PREEMPT_RT). Raleigh, NC. H1B sponsor.",
            "source_url": "https://www.redhat.com/en/about/company",
            "suggested_next_step": "follow_company",
        },
        "Lumen Technologies": {
            "name": "Lumen Technologies",
            "website": "https://www.lumen.com",
            "careers_url": "https://jobs.lumen.com/jobs?keywords=embedded",
            "industry": "Telecom & Networking",
            "summary": "Telecommunications company. Fiber network, edge computing, CDN.",
            "embedded_relevance": "low",
            "research_notes": "Telecom network equipment firmware. Embedded Linux, "
            "DPDK, SDN. Denver, CO. H1B sponsor.",
            "source_url": "https://www.lumen.com/en-us/about.html",
            "suggested_next_step": "monitor_weekly",
        },
        # ── Remaining H1B CSV Companies ─────────────────────────────
        # These companies are primarily software/consulting/cloud and have
        # little to no embedded firmware presence, but are included for
        # completeness since they appear in the H1B sponsor CSV.
        "Accenture": {
            "name": "Accenture",
            "website": "https://www.accenture.com",
            "careers_url": "https://www.accenture.com/us-en/careers/search?keywords=embedded",
            "industry": "IT Consulting",
            "summary": "Global professional services and consulting company.",
            "embedded_relevance": "low",
            "research_notes": "Primarily consulting and IT services. Occasional embedded project roles "
            "through client engagements (automotive, industrial). H1B sponsor.",
            "source_url": "https://www.accenture.com/us-en/about/company-index",
            "suggested_next_step": "monitor_weekly",
        },
        "Adobe": {
            "name": "Adobe",
            "website": "https://www.adobe.com",
            "careers_url": "https://www.adobe.com/careers/search?keywords=embedded",
            "industry": "Software - Creative & Document",
            "summary": "Creative software company. Photoshop, Illustrator, Acrobat, Experience Cloud.",
            "embedded_relevance": "low",
            "research_notes": "Software-focused, no significant embedded/firmware roles. "
            "Occasional low-level systems/rendering roles. H1B sponsor.",
            "source_url": "https://www.adobe.com/about-adobe.html",
            "suggested_next_step": "monitor_weekly",
        },
        "Airbnb": {
            "name": "Airbnb",
            "website": "https://www.airbnb.com",
            "careers_url": "https://careers.airbnb.com/jobs?keywords=embedded",
            "industry": "Travel & Hospitality Platform",
            "summary": "Online marketplace for short-term lodging and experiences.",
            "embedded_relevance": "low",
            "research_notes": "Web/mobile platform company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://news.airbnb.com/about-us/",
            "suggested_next_step": "monitor_weekly",
        },
        "Anthropic": {
            "name": "Anthropic",
            "website": "https://www.anthropic.com",
            "careers_url": "https://www.anthropic.com/careers?keywords=embedded",
            "industry": "AI Research",
            "summary": "AI safety company. Developers of Claude AI assistant.",
            "embedded_relevance": "low",
            "research_notes": "AI/ML research focused. No embedded firmware roles. "
            "Possible edge AI inference roles in future. H1B sponsor.",
            "source_url": "https://www.anthropic.com/company",
            "suggested_next_step": "monitor_weekly",
        },
        "Atlassian": {
            "name": "Atlassian",
            "website": "https://www.atlassian.com",
            "careers_url": "https://jobs.lever.co/atlassian?search=embedded",
            "industry": "Software - Developer Tools",
            "summary": "Collaboration and developer tools. Jira, Confluence, Bitbucket.",
            "embedded_relevance": "low",
            "research_notes": "Software tools company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.atlassian.com/company",
            "suggested_next_step": "monitor_weekly",
        },
        "Bloomberg": {
            "name": "Bloomberg",
            "website": "https://www.bloomberg.com",
            "careers_url": "https://careers.bloomberg.com/jobs?keywords=embedded",
            "industry": "Financial Data & Media",
            "summary": "Financial data, software, and media company. Bloomberg Terminal.",
            "embedded_relevance": "low",
            "research_notes": "Financial software. Some low-level systems/networking roles "
            "but not traditional embedded firmware. H1B sponsor.",
            "source_url": "https://www.bloomberg.com/company/",
            "suggested_next_step": "monitor_weekly",
        },
        "Canva": {
            "name": "Canva",
            "website": "https://www.canva.com",
            "careers_url": "https://boards.greenhouse.io/canva?query=embedded",
            "industry": "Software - Design",
            "summary": "Online graphic design platform.",
            "embedded_relevance": "low",
            "research_notes": "Web design tool company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.canva.com/about/",
            "suggested_next_step": "monitor_weekly",
        },
        "Capgemini": {
            "name": "Capgemini",
            "website": "https://www.capgemini.com",
            "careers_url": "https://careers.capgemini.com/jobs?keywords=embedded",
            "industry": "IT Consulting & Services",
            "summary": "Global IT consulting and services company.",
            "embedded_relevance": "low",
            "research_notes": "IT consulting. Some embedded roles through automotive/industrial "
            "client projects (AUTOSAR, vehicle SW). H1B sponsor.",
            "source_url": "https://www.capgemini.com/about-us/",
            "suggested_next_step": "monitor_weekly",
        },
        "Cognizant Technology Solutions": {
            "name": "Cognizant Technology Solutions",
            "website": "https://www.cognizant.com",
            "careers_url": "https://careers.cognizant.com/jobs?keywords=embedded",
            "industry": "IT Services & Consulting",
            "summary": "IT services and consulting multinational.",
            "embedded_relevance": "low",
            "research_notes": "IT services. Some embedded roles through client projects "
            "(automotive, manufacturing). H1B sponsor.",
            "source_url": "https://www.cognizant.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Databricks": {
            "name": "Databricks",
            "website": "https://www.databricks.com",
            "careers_url": "https://databricks.wd3.myworkdayjobs.com/External/job?keywords=embedded",
            "industry": "Data & AI Platform",
            "summary": "Unified data analytics platform. Lakehouse architecture.",
            "embedded_relevance": "low",
            "research_notes": "Cloud data platform. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.databricks.com/company/about-us",
            "suggested_next_step": "monitor_weekly",
        },
        "Deloitte": {
            "name": "Deloitte",
            "website": "https://www.deloitte.com",
            "careers_url": "https://jobs2.deloitte.com/search-jobs?keywords=embedded",
            "industry": "Professional Services & Consulting",
            "summary": "Global professional services firm. Audit, consulting, tax, advisory.",
            "embedded_relevance": "low",
            "research_notes": "Consulting firm. Occasional embedded systems consulting roles "
            "for defense/industrial clients. H1B sponsor.",
            "source_url": "https://www2.deloitte.com/us/en/pages/about-deloitte/articles/about-deloitte.html",
            "suggested_next_step": "monitor_weekly",
        },
        "Dropbox": {
            "name": "Dropbox",
            "website": "https://www.dropbox.com",
            "careers_url": "https://boards.greenhouse.io/dropbox?query=embedded",
            "industry": "Cloud Storage",
            "summary": "Cloud file hosting and collaboration platform.",
            "embedded_relevance": "low",
            "research_notes": "Cloud software company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.dropbox.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Elastic": {
            "name": "Elastic",
            "website": "https://www.elastic.co",
            "careers_url": "https://elasticsearch.wd3.myworkdayjobs.com/External/job?keywords=embedded",
            "industry": "Search & Observability Software",
            "summary": "Search, observability, and security platform. Elasticsearch.",
            "embedded_relevance": "low",
            "research_notes": "Search/analytics platform. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.elastic.co/about/",
            "suggested_next_step": "monitor_weekly",
        },
        "Electronic Arts": {
            "name": "Electronic Arts",
            "website": "https://www.ea.com",
            "careers_url": "https://jobs.ea.com/jobs?keywords=embedded",
            "industry": "Video Games",
            "summary": "Video game publisher. FIFA, Madden, Battlefield, The Sims.",
            "embedded_relevance": "low",
            "research_notes": "Game company. Some low-level engine/platform roles but not "
            "traditional embedded firmware. H1B sponsor.",
            "source_url": "https://www.ea.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Epic Games": {
            "name": "Epic Games",
            "website": "https://www.epicgames.com",
            "careers_url": "https://www.epicgames.com/site/en-US/careers?keywords=embedded",
            "industry": "Video Games & Game Engine",
            "summary": "Game developer and Unreal Engine creator. Fortnite.",
            "embedded_relevance": "low",
            "research_notes": "Game/engine company. Console platform integration roles "
            "exist but very different from traditional embedded. H1B sponsor.",
            "source_url": "https://www.epicgames.com/site/en-US/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Ernst & Young (EY)": {
            "name": "Ernst & Young (EY)",
            "website": "https://www.ey.com",
            "careers_url": "https://eyu.taleo.net/careersection/ext_us/jobsearch.ftl?keyword=embedded",
            "industry": "Professional Services",
            "summary": "Global professional services firm. Audit, tax, consulting, strategy.",
            "embedded_relevance": "low",
            "research_notes": "Professional services. No embedded roles. H1B sponsor.",
            "source_url": "https://www.ey.com/en_us/about-us",
            "suggested_next_step": "monitor_weekly",
        },
        "Figma": {
            "name": "Figma",
            "website": "https://www.figma.com",
            "careers_url": "https://boards.greenhouse.io/figma?query=embedded",
            "industry": "Software - Design Tools",
            "summary": "Collaborative design tool for UI/UX design.",
            "embedded_relevance": "low",
            "research_notes": "Web design tool. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.figma.com/about/",
            "suggested_next_step": "monitor_weekly",
        },
        "Gusto": {
            "name": "Gusto",
            "website": "https://gusto.com",
            "careers_url": "https://boards.greenhouse.io/gusto?query=embedded",
            "industry": "HR & Payroll Software",
            "summary": "Payroll, benefits, and HR platform for small businesses.",
            "embedded_relevance": "low",
            "research_notes": "HR/payroll SaaS. No embedded roles. H1B sponsor.",
            "source_url": "https://gusto.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "HCL Technologies": {
            "name": "HCL Technologies",
            "website": "https://www.hcltech.com",
            "careers_url": "https://hcl.software.rfe.co/HCL/External/careers?keywords=embedded",
            "industry": "IT Services",
            "summary": "Global IT services and consulting company.",
            "embedded_relevance": "low",
            "research_notes": "IT services. Some embedded roles through automotive/industrial "
            "client projects. H1B sponsor.",
            "source_url": "https://www.hcltech.com/about-us",
            "suggested_next_step": "monitor_weekly",
        },
        "Infosys": {
            "name": "Infosys",
            "website": "https://www.infosys.com",
            "careers_url": "https://careers.infosys.com/search?keyword=embedded",
            "industry": "IT Services & Consulting",
            "summary": "Global IT services, consulting, and business solutions company.",
            "embedded_relevance": "low",
            "research_notes": "IT services. Some embedded design services for automotive "
            "and industrial clients. H1B sponsor.",
            "source_url": "https://www.infosys.com/about.html",
            "suggested_next_step": "monitor_weekly",
        },
        "John Deere": {
            "name": "John Deere",
            "website": "https://www.deere.com",
            "careers_url": "https://jobs.deere.com/search-jobs?keywords=embedded",
            "industry": "Agricultural & Construction Equipment",
            "summary": "See 'Deere & Company'. Same company, alternate name.",
            "embedded_relevance": "high",
            "research_notes": "Same as Deere & Company. Major embedded software employer. "
            "CAN/J1939, autonomy, precision ag.",
            "source_url": "https://www.deere.com/en/our-company/",
            "suggested_next_step": "apply_now",
        },
        "LinkedIn": {
            "name": "LinkedIn",
            "website": "https://www.linkedin.com",
            "careers_url": "https://careers.linkedin.com/jobs/search?keywords=embedded",
            "industry": "Social Networking - Professional",
            "summary": "Professional networking platform (Microsoft subsidiary).",
            "embedded_relevance": "low",
            "research_notes": "Social media platform. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://about.linkedin.com/",
            "suggested_next_step": "monitor_weekly",
        },
        "Lyft": {
            "name": "Lyft",
            "website": "https://www.lyft.com",
            "careers_url": "https://boards.greenhouse.io/lyft?query=embedded",
            "industry": "Rideshare & Transportation",
            "summary": "Rideshare and transportation platform.",
            "embedded_relevance": "low",
            "research_notes": "Rideshare platform. Previously had autonomous vehicle team "
            "(sold to Toyota). Limited embedded roles now. H1B sponsor.",
            "source_url": "https://www.lyft.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "MongoDB": {
            "name": "MongoDB",
            "website": "https://www.mongodb.com",
            "careers_url": "https://jobs.lever.co/mongodb?query=embedded",
            "industry": "Database Software",
            "summary": "NoSQL document database company.",
            "embedded_relevance": "low",
            "research_notes": "Database company. 'Embedded' in MongoDB context refers to "
            "embedded documents (data), not firmware. H1B sponsor.",
            "source_url": "https://www.mongodb.com/company",
            "suggested_next_step": "monitor_weekly",
        },
        "PayPal": {
            "name": "PayPal",
            "website": "https://www.paypal.com",
            "careers_url": "https://jobs.paypal-corp.com/search?keywords=embedded",
            "industry": "Fintech - Payments",
            "summary": "Digital payments and financial technology company.",
            "embedded_relevance": "low",
            "research_notes": "Payment platform. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://about.pypl.com/",
            "suggested_next_step": "monitor_weekly",
        },
        "QVC": {
            "name": "QVC",
            "website": "https://www.qvc.com",
            "careers_url": "https://jobs.qvc.com/search-jobs?keywords=embedded",
            "industry": "Retail & E-commerce",
            "summary": "Video and e-commerce retailer (Qurate Retail Group).",
            "embedded_relevance": "low",
            "research_notes": "Retail company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.qurateretailgroup.com/about-us/",
            "suggested_next_step": "monitor_weekly",
        },
        "SanDisk": {
            "name": "SanDisk",
            "website": "https://www.westerndigital.com",
            "careers_url": "https://jobs.westerndigital.com/search-jobs?keywords=embedded",
            "industry": "Data Storage",
            "summary": "Flash storage brand (now part of Western Digital).",
            "embedded_relevance": "medium",
            "research_notes": "Now part of Western Digital. See Western Digital entry. "
            "Flash controller firmware roles. H1B sponsor.",
            "source_url": "https://www.westerndigital.com/brand/sandisk",
            "suggested_next_step": "follow_company",
        },
        "Savant": {
            "name": "Savant",
            "website": "https://www.savant.com",
            "careers_url": "https://jobs.savant.com/search?keywords=embedded",
            "industry": "Smart Home Technology",
            "summary": "Premium smart home automation systems.",
            "embedded_relevance": "medium",
            "research_notes": "Smart home embedded systems. Lighting/climate/AV control. "
            "Potential embedded firmware roles. Small company. H1B sponsor.",
            "source_url": "https://www.savant.com/about",
            "suggested_next_step": "follow_company",
        },
        "SoftBank": {
            "name": "SoftBank",
            "website": "https://www.softbank.jp",
            "careers_url": "https://www.softbank.jp/en/corp/group/sbm/careers/search?keywords=embedded",
            "industry": "Telecom & Investment",
            "summary": "Japanese conglomerate. Telecom, Vision Fund investments, ARM (formerly).",
            "embedded_relevance": "low",
            "research_notes": "Investment/telecom conglomerate. Previously owned ARM. "
            "Limited direct embedded roles in US. H1B sponsor.",
            "source_url": "https://group.softbank/en/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Symantec": {
            "name": "Symantec",
            "website": "https://www.broadcom.com",
            "careers_url": "https://www.broadcom.com/company/newsroom/press-releases?keywords=embedded",
            "industry": "Cybersecurity",
            "summary": "Enterprise security brand (now part of Broadcom).",
            "embedded_relevance": "low",
            "research_notes": "Now part of Broadcom. See Broadcom entry. "
            "Security software, not embedded firmware. H1B sponsor.",
            "source_url": "https://www.broadcom.com/company/about-us",
            "suggested_next_step": "monitor_weekly",
        },
        "TikTok": {
            "name": "TikTok",
            "website": "https://www.tiktok.com",
            "careers_url": "https://careers.tiktok.com/en/search?keyword=embedded",
            "industry": "Social Media",
            "summary": "Short-form video social media platform (ByteDance).",
            "embedded_relevance": "low",
            "research_notes": "Social media platform. No embedded firmware roles. "
            "Some infra/systems roles. H1B sponsor.",
            "source_url": "https://www.tiktok.com/about",
            "suggested_next_step": "monitor_weekly",
        },
        "Twilio": {
            "name": "Twilio",
            "website": "https://www.twilio.com",
            "careers_url": "https://www.twilio.com/company/jobs?search=embedded",
            "industry": "Cloud Communications",
            "summary": "Cloud communications platform. APIs for voice, messaging, video.",
            "embedded_relevance": "low",
            "research_notes": "Cloud communications. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.twilio.com/company",
            "suggested_next_step": "monitor_weekly",
        },
        "Uber": {
            "name": "Uber",
            "website": "https://www.uber.com",
            "careers_url": "https://www.uber.com/global/en/careers/search?keywords=embedded",
            "industry": "Rideshare & Delivery",
            "summary": "Rideshare, delivery, and freight platform.",
            "embedded_relevance": "low",
            "research_notes": "Platform company. Some systems/infra roles but "
            "no traditional embedded firmware. H1B sponsor.",
            "source_url": "https://www.uber.com/us/en/about/",
            "suggested_next_step": "monitor_weekly",
        },
        "Unity Technologies": {
            "name": "Unity Technologies",
            "website": "https://unity.com",
            "careers_url": "https://careers.unity.com/search?keyword=embedded",
            "industry": "Game Engine & Real-time 3D",
            "summary": "Real-time 3D development platform. Unity engine for games and simulation.",
            "embedded_relevance": "low",
            "research_notes": "Game engine company. Some platform/systems roles but "
            "not traditional embedded. Automotive simulation possible. H1B sponsor.",
            "source_url": "https://unity.com/our-company",
            "suggested_next_step": "monitor_weekly",
        },
        "Wayfair": {
            "name": "Wayfair",
            "website": "https://www.wayfair.com",
            "careers_url": "https://careers.wayfair.com/search?keywords=embedded",
            "industry": "E-commerce - Furniture",
            "summary": "Online furniture and home goods retailer.",
            "embedded_relevance": "low",
            "research_notes": "E-commerce company. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.aboutwayfair.com/",
            "suggested_next_step": "monitor_weekly",
        },
        "Wipro": {
            "name": "Wipro",
            "website": "https://www.wipro.com",
            "careers_url": "https://careers.wipro.com/search?keyword=embedded",
            "industry": "IT Services & Consulting",
            "summary": "Global IT services and consulting company.",
            "embedded_relevance": "low",
            "research_notes": "IT services. Some embedded design services for "
            "automotive and industrial clients. H1B sponsor.",
            "source_url": "https://www.wipro.com/about-us/",
            "suggested_next_step": "monitor_weekly",
        },
        "Zillow": {
            "name": "Zillow",
            "website": "https://www.zillow.com",
            "careers_url": "https://boards.greenhouse.io/zillow?query=embedded",
            "industry": "Real Estate Technology",
            "summary": "Online real estate marketplace.",
            "embedded_relevance": "low",
            "research_notes": "Real estate platform. No embedded firmware roles. H1B sponsor.",
            "source_url": "https://www.zillow.com/z/corp/about/",
            "suggested_next_step": "monitor_weekly",
        },
    }

    def research(self, company_name: str) -> CompanyInput | None:
        data = self._DATA.get(company_name)
        if data:
            return CompanyInput(**data)
        # Return minimal record for unknown companies
        return CompanyInput(
            name=company_name,
            embedded_relevance="unknown",
            research_notes="No research data available. TODO: integrate real research source.",
            suggested_next_step="monitor_weekly",
        )


# TODO: Implement PublicWebResearchSource
# This adapter would:
# 1. Fetch the company's public website via httpx
# 2. Extract relevant information from about/careers pages
# 3. Respect robots.txt
# 4. Return structured CompanyInput
#
# class PublicWebResearchSource(ResearchSource):
#     ...


def get_research_source() -> ResearchSource:
    """Return the configured research source."""
    return MockResearchSource()
