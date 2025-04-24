from manimlib import *

class CyberAttacksPieChart(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Create title based on the statistics
        title = Text("TOTAL CYBER ATTACKS - 800,944 REPORTED INCIDENTS (2024)", 
                    font_size=28, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.6)
        
        # Data for full pie chart
        cyber_attack_data = [
            {"name": "PHISHING", "percentage": 41, "color": "#3498db"},  # Blue
            {"name": "PERSONAL DATA BREACHES", "percentage": 15, "color": "#e74c3c"},  # Red
            {"name": "NON-PAYMENT/DELIVERY", "percentage": 13, "color": "#2ecc71"},  # Green
            {"name": "INVESTMENT SCAMS", "percentage": 10, "color": "#f1c40f"},  # Yellow
            {"name": "IDENTITY THEFT", "percentage": 9, "color": "#9b59b6"},  # Purple
            {"name": "TERRORIST ATTACKS", "percentage": 3, "color": "#e67e22"},  # Orange
            {"name": "OTHER", "percentage": 9, "color": "#7f8c8d"},  # Gray
        ]
        
        # Create full pie chart
        radius = 3.0
        full_pie = VGroup()
        
        # Calculate angles
        total = sum(data["percentage"] for data in cyber_attack_data)
        angles = [data["percentage"] / total * 2 * PI for data in cyber_attack_data]
        
        # Starting angle
        start_angle = 0
        
        # For storing the terrorist sector specifically
        terrorist_sector = None
        terrorist_index = None
        mid_angles = []  # Store all mid angles for labels
        
        # Create sectors for full pie
        for i, (data, angle) in enumerate(zip(cyber_attack_data, angles)):
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=radius,
                start_angle=start_angle,
                angle=angle,
                fill_color=data["color"],
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # Save the mid angle for this sector
            mid_angle = start_angle + angle/2
            mid_angles.append(mid_angle)
            
            # Save the terrorist sector and its index
            if data["name"] == "TERRORIST ATTACKS":
                terrorist_sector = sector
                terrorist_index = i
            
            full_pie.add(sector)
            start_angle += angle
        
        # Position pie chart
        full_pie.move_to(ORIGIN)
        
        # Create percentages only
        percentages = VGroup()
        
        # Start angle for percentage positioning
        start_angle = 0
        
        # For storing the terrorist percentage
        terrorist_percentage = None
        
        # Create percentages for sectors
        for i, (data, angle) in enumerate(zip(cyber_attack_data, angles)):
            mid_angle = start_angle + angle/2
            
            # Calculate position based on angle
            label_dir = np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            
            # Position percentages
            percentage_distance = radius * 0.7
            
            # Create percentage
            percentage = Text(f"{data['percentage']}%", font_size=16, weight=BOLD, color=WHITE)
            
            # Position percentage
            percentage_pos = percentage_distance * label_dir
            percentage.move_to(percentage_pos)
            
            # Save terrorist percentage
            if data["name"] == "TERRORIST ATTACKS":
                terrorist_percentage = percentage
            
            percentages.add(percentage)
            
            start_angle += angle
        
        # Create labels and connector lines for all slices
        labels = VGroup()
        connector_lines = VGroup()
        
        for i, (data, mid_angle) in enumerate(zip(cyber_attack_data, mid_angles)):
            # Calculate direction for label placement
            label_dir = np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            
            # Create label with appropriate color
            label = Text(data["name"], font_size=16, weight=BOLD, color=data["color"])
            
            # Position label closer to the pie chart
            label_distance = radius * 1.3  # Reduced from 1.7 to bring labels closer
            label_pos = label_distance * label_dir
            
            # Adjust label position for better layout
            if data["name"] == "PHISHING" or data["name"] == "PERSONAL DATA BREACHES":
                # These labels may be longer, adjust position slightly
                label_pos += UP * 0.1  # Reduced vertical adjustment
            elif data["name"] == "NON-PAYMENT/DELIVERY":
                label_pos += DOWN * 0.1 + RIGHT * 0.1  # Reduced adjustment
                
            label.move_to(label_pos)
            
            # Create connector line with adjusted end point
            line_start = (radius * 1.05) * label_dir  # Just outside the slice
            line_end = (radius * 1.2) * label_dir     # Reduced from 1.4 to match closer labels
            connector_line = Line(line_start, line_end, color=data["color"], stroke_width=2)
            
            labels.add(label)
            connector_lines.add(connector_line)
        
        # Animation sequence
        self.play(
            Write(title),
            run_time=1
        )
        self.wait(0.5)
        
        # Animate the pie chart creation
        self.play(
            FadeIn(full_pie),
            run_time=1.5
        )
        
        # Show percentages
        self.play(
            FadeIn(percentages),
            run_time=1.5
        )
        
        # Show all labels with connector lines
        self.play(
            *[ShowCreation(line) for line in connector_lines],
            run_time=1
        )
        
        self.play(
            *[Write(label) for label in labels],
            run_time=1.5
        )
        
        self.wait(2)
        
        # Zoom in / focus on terrorist attacks
        # Fade others and keep the terrorist sector
        for i, sector in enumerate(full_pie):
            if i != terrorist_index:
                self.play(
                    sector.animate.set_fill(opacity=0.2),
                    percentages[i].animate.set_fill(opacity=0.2),
                    labels[i].animate.set_fill(opacity=0.2),
                    connector_lines[i].animate.set_stroke(opacity=0.2),
                    run_time=0.1
                )
        
        # Wait a bit longer to let the final scene be visible
        self.wait(5)
        
        # No fade out - everything remains visible at the end
        
class CyberStatisticsScene(Scene):
    """This scene can be expanded in the future to show more cyber attack statistics"""
    def construct(self):
        text = Text("For more detailed statistics on cyber attacks\nvisit us at cybersecurity.gov", 
                   font_size=30, weight=BOLD)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
