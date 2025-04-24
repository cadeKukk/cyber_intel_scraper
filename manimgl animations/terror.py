from manimlib import *

class AttackOriginsPieChart(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Create origin data with the same colors as the image
        origin_data = [
            {"name": "RUSSIA", "percentage": 32, "color": "#3498db"},  # Blue
            {"name": "CHINA", "percentage": 28, "color": "#16a085"},   # Green
            {"name": "IRAN", "percentage": 18, "color": "#d4b00e"},     # Gold/Yellow
            {"name": "NORTH KOREA", "percentage": 12, "color": "#e67e22"}, # Orange
            {"name": "OTHER", "percentage": 10, "color": "#5E35A8"}  # Purple
        ]
        
        # Calculate angles for pie chart sections
        total = sum(data["percentage"] for data in origin_data)
        angles = [data["percentage"] / total * 2 * PI for data in origin_data]
        
        # Create pie chart as a whole with labels included
        pie_chart_group = VGroup()
        pie_chart = VGroup()
        labels = VGroup()
        label_lines = VGroup()  # New group for label lines
        
        # Starting angle (0 is at the right, PI/2 is at the top)
        start_angle = PI/2
        radius = 1.8  # Slightly smaller radius
        
        # Create the pie slices and labels
        for i, (data, angle) in enumerate(zip(origin_data, angles)):
            # Create sector
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
            
            # Calculate mid-angle of the sector
            mid_angle = start_angle + angle/2
            
            # Position for label based on mid-angle
            # Fine-tuned label positions with increased distance for larger text
            if i == 0:  # Russia - top right
                label_pos = radius * 1.4 * np.array([np.cos(mid_angle+0.1), np.sin(mid_angle+0.1), 0])
            elif i == 1:  # China - left
                label_pos = radius * 1.4 * np.array([np.cos(mid_angle-0.3), np.sin(mid_angle-0.3), 0])
            elif i == 2:  # Iran - bottom left
                label_pos = radius * 1.4 * np.array([np.cos(mid_angle-0.1), np.sin(mid_angle-0.1), 0])
            elif i == 3:  # North Korea - bottom right
                label_pos = radius * 1.6 * np.array([np.cos(mid_angle+0.15), np.sin(mid_angle+0.15), 0])
            else:  # Non-state Actors - right
                label_pos = radius * 1.4 * np.array([np.cos(mid_angle+0.05), np.sin(mid_angle+0.05), 0])
            
            # Create combined label with both name and percentage - ALL CAPS and BOLD
            # Increased font size to match nation-state actor labels (size 20)
            label_text = f"{data['name']}: {data['percentage']}%"
            label = Text(label_text, font_size=20, weight=BOLD, color=data["color"])
            
            # Move to position
            label.move_to(label_pos)
            
            # Calculate points for the label line
            edge_point = radius * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            
            # Calculate the direction from pie to label
            direction = label_pos - edge_point
            direction = direction / np.linalg.norm(direction)
            
            # Get the starting point at the edge of the pie
            start_point = edge_point
            
            # Calculate the endpoint for the line
            offset_distance = 0.25  # Consistent small offset distance
            
            # Special case for Russia - adjust the end point to be lower to avoid overlapping with text
            if i == 0:  # Russia
                # Move the end point down and slightly to the left
                end_point = label_pos - direction * offset_distance + np.array([0, -0.15, 0])
            else:
                # For other labels, use standard offset
                end_point = label_pos - direction * offset_distance
            
            # Create label line that connects to near the label
            label_line = Line(
                start_point, 
                end_point,
                color=data["color"],
                stroke_width=2
            )
            
            pie_chart.add(sector)
            labels.add(label)
            label_lines.add(label_line)  # Add the label line to the group
            
            # Update starting angle for next sector
            start_angle += angle
        
        # Group pie chart, label lines, and labels together
        pie_chart_group.add(pie_chart, label_lines, labels)
        
        # Position the pie chart to take up the right half of the frame and move it up slightly
        pie_chart_group.move_to(RIGHT * 3.5 + UP * 0.2)  # Moved further right
        
        # Add section showing primary nation-state actors (similar to the bottom part of image)
        nations_section = VGroup()
        
        # ALL CAPS and BOLD title
        nations_title = Text("PRIMARY NATION-STATE ACTORS", font_size=26, weight=BOLD, color=WHITE)
        
        nations_data = [
            {"name": "RUSSIA (32%)", "subtext": "APT28 (FANCY BEAR), APT29 (COZY BEAR)", "color": "#3498db", "percent": 32},
            {"name": "CHINA (28%)", "subtext": "APT41, APT10", "color": "#16a085", "percent": 28},
            {"name": "IRAN (18%)", "subtext": "APT33 (ELFIN), APT35 (CHARMING KITTEN)", "color": "#d4b00e", "percent": 18},
            {"name": "NORTH KOREA (12%)", "subtext": "LAZARUS GROUP", "color": "#e67e22", "percent": 12},
            {"name": "OTHER (10%)", "subtext": "HACKTIVISTS, CRIMINAL ORGANIZATIONS", "color": "#5E35A8", "percent": 10}
        ]
        
        nations_items = VGroup()
        
        for i, data in enumerate(nations_data):
            item_group = VGroup()
            
            # ALL CAPS and BOLD title
            item_title = Text(data["name"], font_size=20, weight=BOLD, color=WHITE)
            
            # ALL CAPS subtext
            item_subtext = Text(data["subtext"], font_size=16, color="#888888", weight=BOLD)
            item_subtext.next_to(item_title, DOWN, aligned_edge=LEFT, buff=0.05)
            
            # Add progress bar with increased width
            bar_width = 6  # Slightly wider bars
            bar_bg = Rectangle(height=0.12, width=bar_width, fill_color="#333333", fill_opacity=1, stroke_width=0)
            bar_fg_width = bar_width * data["percent"]/100
            bar_fg = Rectangle(
                height=0.12, 
                width=bar_fg_width, 
                fill_color=data["color"], 
                fill_opacity=1, 
                stroke_width=0
            )
            bar_bg.next_to(item_subtext, DOWN, aligned_edge=LEFT, buff=0.08)
            bar_fg.move_to(bar_bg, aligned_edge=LEFT)
            bar_fg.shift(RIGHT * bar_fg_width/2 - RIGHT * bar_width/2)
            
            item_group.add(item_title, item_subtext, bar_bg, bar_fg)
            item_group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)  # Increased spacing
            nations_items.add(item_group)
        
        # Arrange all nation items vertically with better spacing
        nations_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Position the title at the top with less buffer now that main title is gone
        nations_title.to_edge(UP, buff=0.4)
        nations_items.next_to(nations_title, DOWN, aligned_edge=LEFT, buff=0.4)
        nations_section.add(nations_title, nations_items)
        
        # Position the nations section to take up the left half of the frame
        nations_section.move_to(LEFT * 3.0)  # Centered in left half
        
        # Animation sequence - updated to show pie chart and labels first
        self.play(
            FadeIn(pie_chart),
            run_time=1
        )
        
        self.play(
            FadeIn(label_lines),  # Add animation for label lines
            FadeIn(labels),
            run_time=1
        )
        
        # Short pause before showing the nations section
        self.wait(0.5)
        
        # Then show the nations section elements
        self.play(
            Write(nations_title),
            run_time=1
        )
        
        self.play(
            FadeIn(nations_items),
            run_time=1.5
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Render the animation directly to a file
    from manimlib.cli import main
    import sys
    sys.argv = ['terror.py', 'StateVsNonStateCyberAttacks', 'AttackOriginsPieChart', '-o']
    main()
