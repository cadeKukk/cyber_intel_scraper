from manimlib import *

class CyberThreatTiers(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Create a group for everything that will be scaled
        everything = VGroup()
        
        # Define colors for tiers
        HIGH_COLOR = "#E6007E"    # Magenta
        MED_COLOR = "#FFB800"     # Gold
        LOW_COLOR = "#00A3A3"     # Teal
        HIGHLIGHT_COLOR = "#FF0000"  # Bright red for highlighting
        
        # Create tier boxes - with more vertical spacing
        high_box = Rectangle(height=2.5, width=10, fill_color=HIGH_COLOR, 
                            fill_opacity=0.8, stroke_color=WHITE)
        high_box.move_to(UP*3)  # Moved higher
        
        med_box = Rectangle(height=2.5, width=10, fill_color=MED_COLOR, 
                           fill_opacity=0.8, stroke_color=WHITE)
        med_box.move_to(ORIGIN)  # Stays at center
        
        low_box = Rectangle(height=2.5, width=10, fill_color=LOW_COLOR, 
                           fill_opacity=0.8, stroke_color=WHITE)
        low_box.move_to(DOWN*3)  # Moved lower
        
        # Create tier headers
        high_header = Text("HIGH-TIER THREATS", font_size=32, color=WHITE, weight=BOLD)
        high_header.move_to(high_box.get_top() + DOWN*0.4)
        
        med_header = Text("MEDIUM-TIER THREATS", font_size=32, color=WHITE, weight=BOLD)
        med_header.move_to(med_box.get_top() + DOWN*0.4)
        
        low_header = Text("LOW-TIER THREATS", font_size=32, color=WHITE, weight=BOLD)
        low_header.move_to(low_box.get_top() + DOWN*0.4)
        
        # Create threat items
        high_threats = [
            "NATION-STATE OPERATIONS",
            "CRITICAL INFRASTRUCTURE ATTACKS",
            "SUPPLY CHAIN COMPROMISES"
        ]
        
        med_threats = [
            "CYBER TERRORISM",
            "RANSOMWARE OPERATIONS",
            "DATA INTEGRITY ATTACKS"
        ]
        
        low_threats = [
            "HACKTIVISM",
            "INSIDER THREATS",
            "OPPORTUNISTIC CYBER CRIME"
        ]
        
        # Create VGroups for threat text - positioned with fixed spacing
        high_items = VGroup()
        for i, threat in enumerate(high_threats):
            item = Text(threat, font_size=22, color=WHITE)
            item.move_to(high_header.get_center() + DOWN*0.7 + DOWN*0.5*i)
            high_items.add(item)
        
        med_items = VGroup()
        for i, threat in enumerate(med_threats):
            item = Text(threat, font_size=22, color=WHITE)  # Start all with WHITE
            item.move_to(med_header.get_center() + DOWN*0.7 + DOWN*0.5*i)
            med_items.add(item)
        
        low_items = VGroup()
        for i, threat in enumerate(low_threats):
            item = Text(threat, font_size=22, color=WHITE)
            item.move_to(low_header.get_center() + DOWN*0.7 + DOWN*0.5*i)
            low_items.add(item)
        
        # Create simple circle markers
        high_markers = VGroup()
        for i, item in enumerate(high_items):
            marker = Dot(color=WHITE, radius=0.1)
            marker.next_to(item, LEFT, buff=0.4)
            high_markers.add(marker)
        
        med_markers = VGroup()
        for i, item in enumerate(med_items):
            marker = Dot(color=WHITE, radius=0.1)  # Start all with WHITE
            marker.next_to(item, LEFT, buff=0.4)
            med_markers.add(marker)
            
        low_markers = VGroup()
        for i, item in enumerate(low_items):
            marker = Dot(color=WHITE, radius=0.1)
            marker.next_to(item, LEFT, buff=0.4)
            low_markers.add(marker)
        
        # Add everything to the group
        everything.add(high_box, med_box, low_box)
        everything.add(high_header, med_header, low_header)
        everything.add(high_items, med_items, low_items)
        everything.add(high_markers, med_markers, low_markers)
        
        # Scale down by 15% (scale factor of 0.85)
        everything.scale(0.85)
        
        # Animation sequence
        # Animate high tier
        self.play(FadeIn(high_box), Write(high_header), run_time=1)
        self.play(Write(high_items[0]), FadeIn(high_markers[0]), run_time=0.7)
        self.play(Write(high_items[1]), FadeIn(high_markers[1]), run_time=0.7)
        self.play(Write(high_items[2]), FadeIn(high_markers[2]), run_time=0.7)
        
        self.wait(0.5)
        
        # Animate medium tier
        self.play(FadeIn(med_box), Write(med_header), run_time=1)
        self.play(Write(med_items[0]), FadeIn(med_markers[0]), run_time=0.7)  # Normal animation for all
        self.play(Write(med_items[1]), FadeIn(med_markers[1]), run_time=0.7)
        self.play(Write(med_items[2]), FadeIn(med_markers[2]), run_time=0.7)
        
        self.wait(0.5)
        
        # Animate low tier
        self.play(FadeIn(low_box), Write(low_header), run_time=1)
        self.play(Write(low_items[0]), FadeIn(low_markers[0]), run_time=0.7)
        self.play(Write(low_items[1]), FadeIn(low_markers[1]), run_time=0.7)
        self.play(Write(low_items[2]), FadeIn(low_markers[2]), run_time=0.7)
        
        self.wait(2)
        
        # Final animation - emphasize high tier threats
        self.play(
            high_box.animate.set_fill(opacity=0.9),
            med_box.animate.set_fill(opacity=0.5),
            low_box.animate.set_fill(opacity=0.5),
            run_time=1
        )
        
        self.wait(2)
        
        # After all animations are complete, just change the color of Cyber Terrorism
        # Without any movement or scaling
        self.play(
            med_items[0].animate.set_color(HIGHLIGHT_COLOR),
            med_markers[0].animate.set_color(HIGHLIGHT_COLOR),
            run_time=1
        )
        
        self.wait(3)


class SimpleThreatMatrix(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Create a group for everything that will be scaled
        everything = VGroup()
        
        # Define colors
        HIGH_COLOR = "#E6007E"    # Magenta
        MED_COLOR = "#FFB800"     # Gold
        LOW_COLOR = "#00A3A3"     # Teal
        HIGHLIGHT_COLOR = "#FF0000"  # Bright red for highlighting
        
        # Create title
        title = Text("CYBER THREAT MATRIX", font_size=42, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.7)
        
        # Create matrix
        matrix = VGroup()
        size = 1
        for i in range(5):  # i is impact (bottom to top)
            for j in range(5):  # j is likelihood (left to right)
                square = Square(
                    side_length=size,
                    fill_opacity=0.7,
                    stroke_width=2,
                    stroke_color=WHITE
                )
                
                # Color logic based on position
                if i + j <= 2:  # Bottom left - low risk
                    color = LOW_COLOR
                elif i + j >= 6:  # Top right - high risk
                    color = HIGH_COLOR
                else:  # Middle - medium risk
                    color = MED_COLOR
                
                square.set_fill(color)
                square.move_to([j-2, i-2, 0])
                matrix.add(square)
        
        matrix.move_to(ORIGIN)
        
        # Add axis labels
        impact_text = Text("IMPACT", font_size=28, color=WHITE).next_to(matrix, LEFT, buff=0.5).rotate(90*DEGREES)
        likelihood_text = Text("LIKELIHOOD", font_size=28, color=WHITE).next_to(matrix, DOWN, buff=0.5)
        
        # Define threat positions on matrix
        threats = [
            {"name": "NATION-STATE", "pos": [1.5, 1.5, 0], "tier": "HIGH"},
            {"name": "INFRA ATTACKS", "pos": [0.5, 2, 0], "tier": "HIGH"},
            {"name": "SUPPLY CHAIN", "pos": [1, 1, 0], "tier": "HIGH"},
            {"name": "TERRORISM", "pos": [0, 0.5, 0], "tier": "MED", "highlight": True},
            {"name": "RANSOMWARE", "pos": [1.5, -0.5, 0], "tier": "MED"},
            {"name": "DATA ATTACKS", "pos": [0, 0, 0], "tier": "MED"},
            {"name": "HACKTIVISM", "pos": [-1, -1, 0], "tier": "LOW"},
            {"name": "INSIDER", "pos": [-0.5, -1.5, 0], "tier": "LOW"},
            {"name": "OPPORTUNISTIC", "pos": [-1.5, -2, 0], "tier": "LOW"},
        ]
        
        # Create dots and labels
        threat_dots = VGroup()
        threat_labels = VGroup()
        
        # Variable to store terrorism dot and label indices
        terrorism_index = None
        
        for i, threat in enumerate(threats):
            color = {
                "HIGH": HIGH_COLOR,
                "MED": MED_COLOR,
                "LOW": LOW_COLOR
            }[threat["tier"]]
            
            # Record terrorism index but don't highlight yet
            if threat.get("highlight"):
                terrorism_index = i
                
            dot = Dot(threat["pos"], color=WHITE, radius=0.07)
            label = Text(threat["name"], font_size=16, color=color)
            label.next_to(dot, RIGHT, buff=0.1)
            
            threat_dots.add(dot)
            threat_labels.add(label)
        
        # Add everything to the group
        everything.add(title, matrix, impact_text, likelihood_text)
        everything.add(threat_dots, threat_labels)
        
        # Scale down by 15% (scale factor of 0.85)
        everything.scale(0.85)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        self.play(ShowCreation(matrix), run_time=1.5)
        self.play(Write(impact_text), Write(likelihood_text), run_time=1)
        
        # Show all threat points together
        for i in range(len(threats)):
            self.play(
                FadeIn(threat_dots[i]),
                Write(threat_labels[i]),
                run_time=0.5
            )
        
        self.wait(2)
        
        # Group by tier color
        high_group = VGroup()
        med_group = VGroup()
        low_group = VGroup()
        
        for i, threat in enumerate(threats):
            if threat["tier"] == "HIGH":
                high_group.add(threat_dots[i], threat_labels[i])
            elif threat["tier"] == "MED":
                med_group.add(threat_dots[i], threat_labels[i])
            else:
                low_group.add(threat_dots[i], threat_labels[i])
        
        # Highlight each tier
        self.play(
            high_group.animate.set_color(HIGH_COLOR),
            med_group.animate.set_color(MED_COLOR),
            low_group.animate.set_color(LOW_COLOR),
            run_time=1.5
        )
        
        self.wait(2)
        
        # After everything is done, highlight terrorism without moving it
        if terrorism_index is not None:
            self.play(
                threat_dots[terrorism_index].animate.set_color(HIGHLIGHT_COLOR),
                threat_labels[terrorism_index].animate.set_color(HIGHLIGHT_COLOR),
                run_time=1
            )
        
        self.wait(3)
