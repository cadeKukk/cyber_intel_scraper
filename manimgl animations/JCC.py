from manimlib import *

class CyberSecurityOrgChart(Scene):
    def construct(self):
        # Set a good camera view that shows the entire chart clearly
        self.camera.frame.scale(1.2)  # Keep the same scaling for visibility
        self.camera.frame.shift(DOWN * 1.0)  # Shift the view down by 15%
        
        # Title
        title = Text("U.S. Cybersecurity Organization", font_size=36)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        
        # ===== LEVEL 1: EXECUTIVE BRANCH =====
        executive = self.create_box("EXECUTIVE", WHITE, 2.0, 0.8, font_size=24)
        executive.next_to(title, DOWN, buff=0.7)
        
        # ===== LEVEL 2: MAIN DEPARTMENTS =====
        # Create five main department boxes in different colors
        dept_width, dept_height = 1.8, 0.7
        
        dhs = self.create_box("DHS", BLUE, dept_width, dept_height, "Dept of Homeland Security")
        dod = self.create_box("DoD", GREEN, dept_width, dept_height, "Dept of Defense")
        doj = self.create_box("DoJ", RED, dept_width, dept_height, "Dept of Justice")
        dni = self.create_box("ODNI", YELLOW, dept_width, dept_height, "Office of Dir. National Intelligence")
        state = self.create_box("STATE", PURPLE, dept_width, dept_height, "Dept of State")
        
        # Also create JCC box now, but keep it invisible until later
        jcc = self.create_box("JCC", TEAL, dept_width, dept_height, "Joint Cyber Command")
        
        # Position all departments with enough space for JCC
        departments = VGroup(dhs, dod, doj, dni, state)
        departments.arrange(RIGHT, buff=0.5)
        departments.next_to(executive, DOWN, buff=1.2)
        
        # Position JCC to the right of STATE but make it invisible for now
        jcc.next_to(state, RIGHT, buff=0.5)
        jcc.set_opacity(0)  # Make JCC invisible
        
        # Create connection lines from Executive to visible departments
        # We'll add these to the scene FIRST so they're behind everything
        exec_connections = self.create_connections(executive, departments)
        self.add(exec_connections)  # Add to scene first
        
        # ===== LEVEL 3: SUB-AGENCIES =====
        # DHS sub-agencies (BLUE)
        dhs_agencies = VGroup(
            self.create_box("CISA", BLUE_B, 1.3, 0.6, "Cybersecurity & Infrastructure Security Agency"),
            self.create_box("USSS", BLUE_B, 1.3, 0.6, "U.S. Secret Service"),
            self.create_box("ICE-HSI", BLUE_B, 1.3, 0.6, "Immigration & Customs Enforcement")
        )
        
        # DoD sub-agencies (GREEN)
        dod_agencies = VGroup(
            self.create_box("USCYBERCOM", GREEN_B, 1.3, 0.6, "U.S. Cyber Command"),
            self.create_box("NSA", GREEN_B, 1.3, 0.6, "National Security Agency"),
            self.create_box("DC3", GREEN_B, 1.3, 0.6, "Defense Cyber Crime Center"),
            self.create_box("DISA", GREEN_B, 1.3, 0.6, "Defense Information Systems Agency")
        )
        
        # DoJ sub-agencies (RED)
        fbi_box = self.create_box("FBI", RED_B, 1.3, 0.6, "Federal Bureau of Investigation")
        doj_agencies = VGroup(fbi_box)
        
        # ODNI sub-agencies (YELLOW)
        cia_box = self.create_box("CIA", YELLOW_B, 1.3, 0.6, "Central Intelligence Agency")
        odni_agencies = VGroup(
            cia_box,
            self.create_box("NCTC", YELLOW_B, 1.3, 0.6, "National Counterterrorism Center")
        )
        
        # State sub-agencies (PURPLE)
        state_agencies = VGroup(
            self.create_box("OCC", PURPLE_B, 1.3, 0.6, "Office of Coordinator for Cyber Issues"),
            self.create_box("DSS", PURPLE_B, 1.3, 0.6, "Diplomatic Security Service")
        )
        
        # JCC sub-agencies (TEAL) - create them now but keep invisible
        jcc_agencies = VGroup(
            self.create_box("CERT", TEAL_B, 1.3, 0.6, "Computer Emergency Response Team"),
            self.create_box("NCSN", TEAL_B, 1.3, 0.6, "National Cyber Sensor Network")
        )
        jcc_agencies.set_opacity(0)  # Make invisible for now
        
        # Position sub-agencies in columns under their departments
        self.position_children(dhs, dhs_agencies)
        self.position_children(dod, dod_agencies)
        self.position_children(doj, doj_agencies)
        self.position_children(dni, odni_agencies)
        self.position_children(state, state_agencies)
        self.position_children(jcc, jcc_agencies)
        
        # Create connections from departments to sub-agencies
        # Add these connections to the scene BEFORE adding the boxes
        dept_connections = VGroup()
        dept_connections.add(self.create_connections(dhs, dhs_agencies))
        dept_connections.add(self.create_connections(dod, dod_agencies))
        dept_connections.add(self.create_connections(doj, doj_agencies))
        dept_connections.add(self.create_connections(dni, odni_agencies))
        dept_connections.add(self.create_connections(state, state_agencies))
        self.add(dept_connections)  # Add connections first
        
        # ===== LEVEL 4: SUB-UNITS =====
        # FBI sub-units
        fbi_units = VGroup(
            self.create_box("FBI CYBER", RED_C, 1.1, 0.5, "FBI Cyber Division"),
            self.create_box("NCFTA", RED_C, 1.1, 0.5, "National Cyber-Forensics & Training Alliance")
        )
        self.position_children(fbi_box, fbi_units)
        
        # Create connections from FBI to its sub-units
        unit_connections = self.create_connections(fbi_box, fbi_units)
        self.add(unit_connections)  # Add connections first
        
        # Create single connection line from Executive to JCC (but invisible)
        start = executive.get_bottom()
        end = jcc.get_top()
        jcc_connection = Line(start, end, stroke_color=GREY, stroke_width=1.5)
        jcc_connection.set_opacity(0)  # Make invisible for now
        self.add(jcc_connection)  # Add to scene first
        
        # Create connections from JCC to its sub-agencies (but invisible)
        jcc_dept_connections = self.create_connections(jcc, jcc_agencies)
        jcc_dept_connections.set_opacity(0)  # Make invisible for now
        self.add(jcc_dept_connections)  # Add to scene first
        
        # Now add all boxes on top of the connections
        # Adding them to the scene after the connections ensures they're on top
        self.add(executive)
        self.add(departments)
        self.add(dhs_agencies, dod_agencies, doj_agencies, odni_agencies, state_agencies)
        self.add(fbi_units)
        self.add(jcc, jcc_agencies)
        
        # Create highlight elements (surround boxes)
        cia_highlight = SurroundingRectangle(cia_box, buff=.1, color=YELLOW)
        fbi_highlight = SurroundingRectangle(fbi_box, buff=.1, color=RED)
        
        # Remove all elements to prepare for the animation sequence
        self.remove(
            executive, departments, dhs_agencies, dod_agencies, doj_agencies, 
            odni_agencies, state_agencies, fbi_units, exec_connections, 
            dept_connections, unit_connections, jcc, jcc_agencies, 
            jcc_connection, jcc_dept_connections, cia_highlight, fbi_highlight
        )
        
        # ===== ANIMATION SEQUENCE =====
        # Level 1: Executive Branch
        self.play(FadeIn(executive))
        self.wait(0.3)
        
        # Level 2: Main Departments
        self.play(FadeIn(departments))
        self.play(ShowCreation(exec_connections))
        self.wait(0.3)
        
        # Level 3: Sub-agencies
        all_agencies = VGroup(
            dhs_agencies, dod_agencies, doj_agencies,
            odni_agencies, state_agencies
        )
        self.play(FadeIn(all_agencies))
        self.play(ShowCreation(dept_connections))
        self.wait(0.3)
        
        # Level 4: Sub-units
        self.play(FadeIn(fbi_units))
        self.play(ShowCreation(unit_connections))
        self.wait(0.8)
        
        # First highlight CIA block
        self.play(ShowCreation(cia_highlight), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(cia_highlight), run_time=0.8)
        self.wait(0.5)
        
        # Highlight FBI block
        self.play(ShowCreation(fbi_highlight), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(fbi_highlight), run_time=0.8)
        self.wait(0.5)
        
        # Highlight CIA one more time
        self.play(ShowCreation(cia_highlight), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(cia_highlight), run_time=0.8)
        self.wait(0.5)
        
        # ===== ADDING JCC AFTER ORIGINAL ANIMATION =====
        # Reveal JCC with fade-in animation
        self.play(
            jcc.animate.set_opacity(1),
            run_time=1
        )
        self.play(jcc_connection.animate.set_opacity(1))
        self.wait(0.3)
        
        # Reveal JCC sub-agencies with fade-in animation
        self.play(jcc_agencies.animate.set_opacity(1))
        self.play(jcc_dept_connections.animate.set_opacity(1))
        
        # Final slight shift to center the complete chart
        self.play(
            self.camera.frame.animate.move_to(RIGHT * 0.25 + DOWN * 1.0),
            run_time=1
        )
        self.wait(2)
    
    def create_box(self, acronym, color, width, height, full_name=None, font_size=18):
        """Create a box with acronym and optionally a smaller full name label"""
        # Create the main box with acronym
        rect = Rectangle(width=width, height=height, fill_color=color, 
                         fill_opacity=0.3, stroke_color=color)
        text = Text(acronym, font_size=font_size)
        
        box = VGroup(rect, text)
        
        # Add full name as small text below if provided
        if full_name:
            name_label = Text(full_name, font_size=10)
            # Scale if too wide
            if name_label.get_width() > width * 1.2:
                name_label.scale(width * 1.2 / name_label.get_width())
            name_label.next_to(rect, DOWN, buff=0.05)
            box.add(name_label)
        
        return box
    
    def position_children(self, parent, children):
        """Position children in a vertical column below parent"""
        if len(children) == 0:
            return
            
        children.arrange(DOWN, buff=0.4)
        children.next_to(parent, DOWN, buff=0.8)
    
    def create_connections(self, parent, children):
        """Create straight lines connecting parent to all children"""
        if isinstance(children, VGroup) and len(children) == 0:
            return VGroup()
            
        lines = VGroup()
        
        if isinstance(children, VGroup):
            # Connect parent to multiple children
            for child in children:
                start = parent.get_bottom()
                end = child.get_top()
                line = Line(start, end, stroke_color=GREY, stroke_width=1.5)
                lines.add(line)
        else:
            # Connect parent to a single child
            start = parent.get_bottom()
            end = children.get_top()
            line = Line(start, end, stroke_color=GREY, stroke_width=1.5)
            lines.add(line)
            
        return lines


if __name__ == "__main__":
    # Command to run: manimgl JCC.py CyberSecurityOrgChart
    pass
