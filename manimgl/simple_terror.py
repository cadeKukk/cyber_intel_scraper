from manimlib import *
import sys

class CyberTerrorismScene(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Title
        title = Text("Cyber Terrorism Analysis", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # --- SECTION 1: ATTACK ORIGINS ---
        section_title = Text("Attack Origins", font_size=36)
        section_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(section_title), run_time=1)
        
        # Create origin data
        origin_data = [
            {"name": "Russia", "percentage": 32, "color": "#D22730"},
            {"name": "China", "percentage": 28, "color": "#FFDE00"},
            {"name": "Iran", "percentage": 18, "color": "#239F40"},
            {"name": "North Korea", "percentage": 12, "color": "#3E5C97"},
            {"name": "Non-state Actors", "percentage": 10, "color": "#777777"}
        ]
        
        # Create simple horizontal bars
        bars = VGroup()
        labels = VGroup()
        
        for i, data in enumerate(origin_data):
            # Create bar
            bar = Rectangle(
                height=0.5,
                width=data["percentage"] / 10,
                fill_color=data["color"],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # Position bar
            bar.move_to(DOWN * (i * 0.7 + 2))
            bar.align_to(ORIGIN, LEFT)
            
            # Create label
            label = Text(f"{data['name']}: {data['percentage']}%", font_size=20, color=data["color"])
            label.next_to(bar, RIGHT, buff=0.2)
            
            bars.add(bar)
            labels.add(label)
        
        # Show bars and labels
        self.play(
            *[ShowCreation(bar) for bar in bars],
            run_time=1.5
        )
        self.play(
            *[Write(label) for label in labels],
            run_time=1
        )
        
        self.wait(2)
        
        # Transition out
        self.play(
            FadeOut(bars),
            FadeOut(labels),
            FadeOut(section_title),
            run_time=1
        )
        
        # --- SECTION 2: TARGET SECTORS ---
        section_title = Text("Target Sectors", font_size=36)
        section_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(section_title), run_time=1)
        
        # Create sector data
        sector_data = [
            {"name": "Energy", "percentage": 28, "color": "#F7B801"},
            {"name": "Government", "percentage": 24, "color": "#2D7DD2"},
            {"name": "Financial", "percentage": 17, "color": "#97CC04"},
            {"name": "Healthcare", "percentage": 12, "color": "#F45D01"},
            {"name": "Transportation", "percentage": 10, "color": "#474973"},
            {"name": "Water Systems", "percentage": 9, "color": "#029676"}
        ]
        
        # Create simple text blocks for sectors
        sector_blocks = VGroup()
        
        # Arrange in a grid (2 rows of 3)
        cols, rows = 3, 2
        for i, data in enumerate(sector_data):
            # Calculate position
            col = i % cols
            row = i // cols
            
            # Create colored block
            block = Rectangle(
                height=1.5,
                width=2.5,
                fill_color=data["color"],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # Create text
            text = Text(
                f"{data['name']}\n{data['percentage']}%", 
                font_size=24,
                color=WHITE
            )
            text.move_to(block)
            
            # Group block and text
            group = VGroup(block, text)
            
            # Position in grid
            x_pos = (col - 1) * 3
            y_pos = (row - 0.5) * 2
            group.move_to(RIGHT * x_pos + DOWN * (y_pos + 1.5))
            
            sector_blocks.add(group)
        
        # Show sector blocks
        self.play(
            *[ShowCreation(block[0]) for block in sector_blocks],
            run_time=1.5
        )
        self.play(
            *[Write(block[1]) for block in sector_blocks],
            run_time=1.5
        )
        
        self.wait(2)
        
        # Transition out
        self.play(
            FadeOut(sector_blocks),
            FadeOut(section_title),
            run_time=1
        )
        
        # --- SECTION 3: ATTACK TECHNIQUES ---
        section_title = Text("Attack Techniques", font_size=36)
        section_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(section_title), run_time=1)
        
        # Create technique data
        technique_data = [
            {"name": "Phishing", "percentage": 35, "color": "#6B5B95"},
            {"name": "Malware", "percentage": 28, "color": "#88B04B"},
            {"name": "DDoS", "percentage": 17, "color": "#FF6F61"},
            {"name": "Zero-day", "percentage": 12, "color": "#DD4124"},
            {"name": "Supply Chain", "percentage": 8, "color": "#347B98"}
        ]
        
        # Create simple vertical bars
        bars = VGroup()
        labels = VGroup()
        percentages = VGroup()
        
        spacing = 1.5
        
        for i, data in enumerate(technique_data):
            # Position along x-axis
            x_pos = (i - (len(technique_data) - 1) / 2) * spacing
            
            # Create bar
            bar = Rectangle(
                height=data["percentage"] / 10,
                width=0.8,
                fill_color=data["color"],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # Position from bottom
            bar.move_to(RIGHT * x_pos + DOWN * 2.5)
            bar.align_to(DOWN * 3.5, DOWN)
            
            # Add percentage on top
            percentage = Text(f"{data['percentage']}%", font_size=18)
            percentage.next_to(bar, UP, buff=0.1)
            
            # Add label below
            label = Text(data["name"], font_size=18, color=data["color"])
            label.next_to(bar, DOWN, buff=0.2)
            
            bars.add(bar)
            labels.add(label)
            percentages.add(percentage)
        
        # Show bars
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=1.5
        )
        self.play(
            *[Write(label) for label in labels],
            *[Write(percentage) for percentage in percentages],
            run_time=1
        )
        
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(bars),
            FadeOut(labels),
            FadeOut(percentages),
            FadeOut(section_title),
            run_time=1
        )
        
        # --- CONCLUSION ---
        conclusion = Text("Cyber Threat Summary", font_size=40, weight=BOLD)
        conclusion.next_to(title, DOWN, buff=0.5)
        
        points = VGroup(
            Text("• Nation-state actors account for 90% of sophisticated incidents", font_size=24),
            Text("• Energy sector is the most targeted (28%)", font_size=24),
            Text("• Phishing remains the most common attack vector (35%)", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        points.next_to(conclusion, DOWN, buff=0.5)
        
        self.play(Write(conclusion), run_time=1)
        self.play(Write(points), run_time=2)
        
        self.wait(3)
        
        # Final fade out
        self.play(
            FadeOut(title),
            FadeOut(conclusion),
            FadeOut(points),
            run_time=1.5
        )
        
        self.wait(1)

if __name__ == "__main__":
    # Render the animation directly to a file
    from manimlib.cli import main
    sys.argv = ['simple_terror.py', 'CyberTerrorismScene', '-w']
    main() 