from manimlib import *

class CybersecuritySources(Scene):
    def construct(self):
        # Dark background
        self.camera.background_color = BLACK
        
        # List of sources with acronyms
        sources = [
            "CISA - Cybersecurity & Infrastructure Security Agency",
            "US-CERT - United States Computer Emergency Readiness Team",
            "FBI CD - Federal Bureau of Investigation Cyber Division",
            "NSA CD - National Security Agency Cybersecurity Directorate",
            "USCYBERCOM - United States Cyber Command",
            "NIST CSF - National Institute of Standards & Technology Cybersecurity Framework",
            "DHS CISA - Department of Homeland Security Cybersecurity Agency",
            "SANS ISC - SANS Internet Storm Center",
            "MITRE ATT&CK - MITRE Adversarial Tactics, Techniques & Common Knowledge",
            "NCCoE - National Cybersecurity Center of Excellence",
            "IG - InfraGard",
            "USSS ECTF - US Secret Service Electronic Crimes Task Forces",
            "NGA CC - National Geospatial-Intelligence Agency Cyber Center",
            "DC3 - Defense Cyber Crime Center",
            "CSC - Cybersecurity Coalition",
            "IC3 - Internet Crime Complaint Center",
            "DARPA I2O - Defense Advanced Research Projects Agency Information Innovation Office",
            "CERT/CC - Computer Emergency Response Team Coordination Center",
            "NSA CV - NSA Cyber Vault",
            "USDS - United States Digital Service",
            "DoD CCC - Department of Defense Cyber Crime Center",
            "JTF-CD - Joint Task Force Cyber Defense",
            "CNMF - Cyber National Mission Force",
            "ARCYBER - United States Army Cyber Command",
            "NAVCYBERFOR - Naval Cyber Forces",
            "AFCYBER - Air Forces Cyber",
            "SPFCYBER - Space Force Cyber Operations",
            "CGCYBER - Coast Guard Cyber Command",
            "MARFORCYBER - Marine Corps Forces Cyberspace Command",
            "NCM - National Cryptologic Museum",
            "DEA CIU - Drug Enforcement Administration Cyber Intelligence Unit",
            "CTIIC - Cyber Threat Intelligence Integration Center",
            "DIA CID - Defense Intelligence Agency Cyber Intelligence Division",
            "TSA CSB - Transportation Security Administration Cybersecurity Branch",
            "FEMA CD - Federal Emergency Management Agency Cybersecurity Division",
            "DOE CO - Department of Energy Cybersecurity Office",
            "ICS-CERT - Industrial Control Systems Cyber Emergency Response Team",
            "USCC - US Cyber Challenge",
            "CTA - Cyber Threat Alliance",
            "ACSC - Advanced Cyber Security Center",
            "CIS - Center for Internet Security",
            "NCFTA - National Cyber-Forensics Training Alliance",
            "FS-ISAC - Financial Services Information Sharing and Analysis Center",
            "MS-ISAC - Multi-State Information Sharing and Analysis Center",
            "CWR - Cyber Warfare Range",
            "FIRST - Forum of Incident Response and Security Teams",
            "ISACA - Information Systems Audit and Control Association",
            "ISC² - International Information System Security Certification Consortium",
            "CERT - Computer Emergency Response Team",
            "WPCRC - West Point Cyber Research Center",
            "NPS CAG - Naval Postgraduate School Cyber Academic Group",
            "AFIT - Air Force Institute of Technology",
            "NWC CIPI - Naval War College Cyber & Innovation Policy Institute",
            "SEI - Software Engineering Institute",
            "GTRI - Georgia Tech Research Institute",
            "UMD CyS - University of Maryland Cybersecurity Center",
            "NYU CS - New York University Center for Cybersecurity",
            "NU CyS - Northeastern University Cybersecurity Center",
            "CERIAS - Center for Education and Research in Information Assurance and Security",
            "SCI - Stanford Cyber Initiative"
        ]
        
        # Define clear boundaries for the two sections
        left_section_width = FRAME_WIDTH * 0.55  # Width of the left section for text
        right_section_width = FRAME_WIDTH * 0.45  # Width of the right section for QR code
        
        # Horizontal position for text (centered in left section)
        text_x_position = -right_section_width/2
        
        # Create text list aligned to the left side of screen
        text_group = VGroup()
        for source in sources:
            text = Text(source, font_size=20, color=WHITE)
            # Limit the width of the text to fit in left section
            max_text_width = left_section_width - 1  # Leave some margin
            if text.get_width() > max_text_width:
                text.set_width(max_text_width)
            text_group.add(text)
        
        # Arrange vertically with all text left-aligned
        text_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        # Position text group in left section and ensure full visibility
        text_group.move_to([text_x_position, 0, 0])
        text_group.to_edge(UP)
        
        # Ensure text doesn't get cut off on the left edge
        if text_group.get_left()[0] < -FRAME_WIDTH/2 + 0.5:
            text_group.shift(RIGHT * ((-FRAME_WIDTH/2 + 0.5) - text_group.get_left()[0]))
        
        # Load QR code image
        qr_code = ImageMobject("CYBER.png")
        
        # Set QR code size and position it on the right
        qr_code.height = 4
        qr_code.move_to([FRAME_WIDTH/4, 0, 0])  # Position in right section
        
        # Create a background rectangle for the QR code to ensure no text overlap
        qr_background = Rectangle(
            width=qr_code.get_width() + 1,
            height=qr_code.get_height() + 1,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        qr_background.move_to(qr_code.get_center())
        
        # Add a title for the QR code
        qr_title = Text("Scan for Cybersecurity Resources", font_size=24, color=YELLOW)
        qr_title.next_to(qr_code, UP, buff=0.5)
        
        # Add elements in the correct order to ensure proper visibility
        self.add(qr_background, text_group, qr_code, qr_title)
        
        # Ensure all of the text is visible by starting it lower and scrolling it completely through
        self.play(
            text_group.animate.shift(UP * (text_group.get_height() + FRAME_HEIGHT)),
            rate_func=linear,
            run_time=16
        )
