from manimlib import *

class CyberTerrorTargets(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#111111"
        
        # Create target data with colors
        target_data = [
            {"name": "CRITICAL INFRASTRUCTURE", "percentage": 35, "color": "#e74c3c"},  # Red
            {"name": "GOVERNMENT AGENCIES", "percentage": 25, "color": "#3498db"},     # Blue
            {"name": "FINANCIAL INSTITUTIONS", "percentage": 18, "color": "#f1c40f"},  # Yellow
            {"name": "DEFENSE CONTRACTORS", "percentage": 12, "color": "#16a085"},     # Green
            {"name": "HEALTHCARE", "percentage": 10, "color": "#9b59b6"}               # Purple
        ]
        
        # Calculate angles for pie chart sections
        total = sum(data["percentage"] for data in target_data)
        angles = [data["percentage"] / total * 2 * PI for data in target_data]
        
        # Create pie chart as a whole with labels included
        pie_chart_group = VGroup()
        pie_chart = VGroup()
        labels = VGroup()
        label_lines = VGroup()
        
        # Starting angle (0 is at the right, PI/2 is at the top)
        start_angle = PI/2
        radius = 1.8
        
        # Create the pie slices and labels
        for i, (data, angle) in enumerate(zip(target_data, angles)):
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
            
            # Position for label
            label_pos = radius * 1.5 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            
            # Create combined label with both name and percentage
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
            offset_distance = 0.25
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
            label_lines.add(label_line)
            
            # Update starting angle for next sector
            start_angle += angle
        
        # Group pie chart, label lines, and labels together
        pie_chart_group.add(pie_chart, label_lines, labels)
        
        # Position the pie chart to take up the right half of the frame
        pie_chart_group.move_to(RIGHT * 2.0)
        
        # Add title
        title = Text("TARGETS OF CYBER TERROR ATTACKS AGAINST THE US", 
                    font_size=28, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.3)
        
        # Detailed information about each target
        targets_section = VGroup()
        
        targets_details = [
            {
                "name": "CRITICAL INFRASTRUCTURE (35%)",
                "subtext": "ENERGY GRIDS, WATER SYSTEMS, TRANSPORTATION",
                "details": "• Attacks aimed at disrupting essential services",
                "color": "#e74c3c",
                "percent": 35
            },
            {
                "name": "GOVERNMENT AGENCIES (25%)",
                "subtext": "FEDERAL, STATE, AND LOCAL ENTITIES",
                "details": "• Espionage and data theft operations",
                "color": "#3498db",
                "percent": 25
            },
            {
                "name": "FINANCIAL INSTITUTIONS (18%)",
                "subtext": "BANKS, TRADING PLATFORMS, PAYMENT SYSTEMS",
                "details": "• Targets include banking systems and cryptocurrency exchanges",
                "color": "#f1c40f",
                "percent": 18
            },
            {
                "name": "DEFENSE CONTRACTORS (12%)",
                "subtext": "MILITARY SUPPLIERS AND RESEARCH ORGS",
                "details": "• Intellectual property theft and espionage",
                "color": "#16a085",
                "percent": 12
            },
            {
                "name": "HEALTHCARE (10%)",
                "subtext": "HOSPITALS, RESEARCH LABS, INSURANCE",
                "details": "• Ransom operations and sensitive data theft",
                "color": "#9b59b6",
                "percent": 10
            }
        ]
        
        targets_items = VGroup()
        
        for i, data in enumerate(targets_details):
            item_group = VGroup()
            
            # Title for each target
            item_title = Text(data["name"], font_size=20, weight=BOLD, color=WHITE)
            
            # Subtitle
            item_subtext = Text(data["subtext"], font_size=16, color="#888888", weight=BOLD)
            item_subtext.next_to(item_title, DOWN, aligned_edge=LEFT, buff=0.05)
            
            # Details
            item_details = Text(data["details"], font_size=16, color="#cccccc")
            item_details.next_to(item_subtext, DOWN, aligned_edge=LEFT, buff=0.05)
            
            # Add progress bar
            bar_width = 6
            bar_bg = Rectangle(height=0.12, width=bar_width, fill_color="#333333", fill_opacity=1, stroke_width=0)
            bar_fg_width = bar_width * data["percent"]/100
            bar_fg = Rectangle(
                height=0.12, 
                width=bar_fg_width, 
                fill_color=data["color"], 
                fill_opacity=1, 
                stroke_width=0
            )
            bar_bg.next_to(item_details, DOWN, aligned_edge=LEFT, buff=0.08)
            bar_fg.move_to(bar_bg, aligned_edge=LEFT)
            bar_fg.shift(RIGHT * bar_fg_width/2 - RIGHT * bar_width/2)
            
            item_group.add(item_title, item_subtext, item_details, bar_bg, bar_fg)
            item_group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            targets_items.add(item_group)
        
        # Arrange all target items vertically
        targets_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Position the section in the left part of the screen
        targets_items.scale(0.8)  # Scale down to fit
        targets_items.move_to(LEFT * 4.0 + DOWN * 0.2)
        targets_section.add(targets_items)
        
        # Animation sequence
        self.play(
            Write(title),
            run_time=1
        )
        
        self.play(
            FadeIn(pie_chart),
            run_time=1
        )
        
        self.play(
            FadeIn(label_lines),
            FadeIn(labels),
            run_time=1
        )
        
        # Short pause before showing the targets section
        self.wait(0.5)
        
        # Show the targets section elements
        self.play(
            FadeIn(targets_items),
            run_time=1.5
        )
        
        # Final pause to view the complete visualization
        self.wait(3)
        
        # Create new target data with Critical Infrastructure at 92% and randomized remaining percentages
        new_target_data = [
            {"name": "CRITICAL INFRASTRUCTURE", "percentage": 92, "color": "#e74c3c"},  # Red
            {"name": "GOVERNMENT AGENCIES", "percentage": 3, "color": "#3498db"},      # Blue
            {"name": "FINANCIAL INSTITUTIONS", "percentage": 1, "color": "#f1c40f"},   # Yellow
            {"name": "DEFENSE CONTRACTORS", "percentage": 2.5, "color": "#16a085"},    # Green
            {"name": "HEALTHCARE", "percentage": 1.5, "color": "#9b59b6"}              # Purple
        ]
        
        # Calculate new angles for smooth transition
        new_total = sum(data["percentage"] for data in new_target_data)
        new_angles = [data["percentage"] / new_total * 2 * PI for data in new_target_data]
        
        # Create a completely new pie chart
        new_pie_chart = VGroup()
        new_start_angle = PI/2
        
        # Create the new pie slices
        for i, (data, angle) in enumerate(zip(new_target_data, new_angles)):
            # Create sector with the same style as original
            new_sector = AnnularSector(
                inner_radius=0,
                outer_radius=radius,
                start_angle=new_start_angle,
                angle=angle,
                fill_color=data["color"],
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            new_pie_chart.add(new_sector)
            new_start_angle += angle
        
        # Position the new pie chart at the same position as the original
        new_pie_chart.move_to(pie_chart.get_center())
        
        # Create the Critical Infrastructure label positioned more to the right
        # Use a fixed position to the right of the pie chart instead of angle-based positioning
        ci_label_text = f"{new_target_data[0]['name']}: {new_target_data[0]['percentage']}%"
        ci_label = Text(ci_label_text, font_size=22, weight=BOLD, color=new_target_data[0]["color"])
        
        # Position the label to the right of the pie chart
        ci_label_pos = pie_chart.get_center() + RIGHT * 3.0
        ci_label.move_to(ci_label_pos)
        
        # Add dramatic title change
        new_title = Text("CRITICAL INFRASTRUCTURE: 92% OF MONETARY COST", 
                        font_size=32, weight=BOLD, color="#e74c3c")
        new_title.to_edge(UP, buff=0.3)
        
        # Animate the transition of the pie chart
        self.play(
            # Use Transform to morph from old chart to new chart, keeping them connected
            *[Transform(pie_chart[i], new_pie_chart[i]) for i in range(len(pie_chart))],
            # Fade out all labels and lines
            FadeOut(labels),
            FadeOut(label_lines),
            run_time=2.0
        )
        
        # Add only the Critical Infrastructure label (no line)
        self.play(
            FadeIn(ci_label),
            ReplacementTransform(title, new_title),
            run_time=1.0
        )
        
        # Update the progress bars in targets section with the new randomized percentages
        new_targets_details = [
            {
                "name": "CRITICAL INFRASTRUCTURE (92%)",
                "subtext": "ENERGY GRIDS, WATER SYSTEMS, TRANSPORTATION",
                "details": "• Attacks aimed at disrupting essential services",
                "color": "#e74c3c",
                "percent": 92
            },
            {
                "name": "GOVERNMENT AGENCIES (3%)",
                "subtext": "FEDERAL, STATE, AND LOCAL ENTITIES",
                "details": "• Espionage and data theft operations",
                "color": "#3498db",
                "percent": 3
            },
            {
                "name": "FINANCIAL INSTITUTIONS (1%)",
                "subtext": "BANKS, TRADING PLATFORMS, PAYMENT SYSTEMS",
                "details": "• Targets include banking systems and cryptocurrency exchanges",
                "color": "#f1c40f",
                "percent": 1
            },
            {
                "name": "DEFENSE CONTRACTORS (2.5%)",
                "subtext": "MILITARY SUPPLIERS AND RESEARCH ORGS",
                "details": "• Intellectual property theft and espionage",
                "color": "#16a085",
                "percent": 2.5
            },
            {
                "name": "HEALTHCARE (1.5%)",
                "subtext": "HOSPITALS, RESEARCH LABS, INSURANCE",
                "details": "• Ransom operations and sensitive data theft",
                "color": "#9b59b6",
                "percent": 1.5
            }
        ]
        
        new_targets_items = VGroup()
        
        for i, data in enumerate(new_targets_details):
            item_group = VGroup()
            
            # Title for each target
            item_title = Text(data["name"], font_size=20, weight=BOLD, color=WHITE)
            
            # Subtitle
            item_subtext = Text(data["subtext"], font_size=16, color="#888888", weight=BOLD)
            item_subtext.next_to(item_title, DOWN, aligned_edge=LEFT, buff=0.05)
            
            # Details
            item_details = Text(data["details"], font_size=16, color="#cccccc")
            item_details.next_to(item_subtext, DOWN, aligned_edge=LEFT, buff=0.05)
            
            # Add progress bar
            bar_width = 6
            bar_bg = Rectangle(height=0.12, width=bar_width, fill_color="#333333", fill_opacity=1, stroke_width=0)
            bar_fg_width = bar_width * data["percent"]/100
            bar_fg = Rectangle(
                height=0.12, 
                width=bar_fg_width, 
                fill_color=data["color"], 
                fill_opacity=1, 
                stroke_width=0
            )
            bar_bg.next_to(item_details, DOWN, aligned_edge=LEFT, buff=0.08)
            bar_fg.move_to(bar_bg, aligned_edge=LEFT)
            bar_fg.shift(RIGHT * bar_fg_width/2 - RIGHT * bar_width/2)
            
            item_group.add(item_title, item_subtext, item_details, bar_bg, bar_fg)
            item_group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            new_targets_items.add(item_group)
        
        # Arrange all target items vertically
        new_targets_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        new_targets_items.scale(0.8)
        new_targets_items.move_to(targets_items.get_center())
        
        # Animate the change in the target details
        self.play(
            ReplacementTransform(targets_items, new_targets_items),
            run_time=1.5
        )
        
        # Final pause to view the updated visualization
        self.wait(3)
        
        # Add "STATE SPONSORED" overlay on part of the 92% Critical Infrastructure slice
        # Calculate what percentage of the total is the 81% state sponsored portion
        state_sponsored_percent = 81
        total_ci_percent = 92
        state_sponsored_ratio = state_sponsored_percent / 100  # 81% of the total
        
        # Calculate the angle for the state sponsored portion (81% of total)
        state_sponsored_angle = 2 * PI * state_sponsored_ratio
        
        # Create a semi-transparent overlay sector with angle for 81% of the total
        state_sponsored_sector = AnnularSector(
            inner_radius=0,
            outer_radius=radius,
            start_angle=PI/2,  # Same starting angle as the pie chart
            angle=state_sponsored_angle,  # Use angle for 81% of the total
            fill_color="#ff0000",  # Bright red for emphasis
            fill_opacity=0.4,  # Semi-transparent
            stroke_color=WHITE,
            stroke_width=2  # Thicker stroke for emphasis
        )
        
        # Position the overlay at the same position as the pie chart
        state_sponsored_sector.move_to(pie_chart.get_center())
        
        # Create the STATE SPONSORED label with 81%
        state_sponsored_label = Text("STATE SPONSORED: 81%", 
                            font_size=24, weight=BOLD, color="#ff0000")
        
        # Position the label on top of the state sponsored slice
        # Calculate position based on the middle of the state sponsored sector
        mid_angle = PI/2 + state_sponsored_angle/2
        label_distance = radius * 0.65  # Place it within the slice
        label_pos = pie_chart.get_center() + label_distance * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
        state_sponsored_label.move_to(label_pos)
        
        # Animate the overlay appearance with a dramatic reveal
        self.play(
            FadeIn(state_sponsored_sector, rate_func=rush_into),
            run_time=1.0
        )
        
        self.play(
            Write(state_sponsored_label),
            run_time=1.0
        )
        
        # Update the title to include state sponsorship information
        final_title = Text("CRITICAL INFRASTRUCTURE: 81% STATE SPONSORED ATTACKS", 
                          font_size=32, weight=BOLD, color="#ff0000")
        final_title.to_edge(UP, buff=0.3)
        
        self.play(
            ReplacementTransform(new_title, final_title),
            run_time=1.0
        )
        
        # Final pause to view the complete visualization with state sponsorship overlay
        self.wait(3)

if __name__ == "__main__":
    # Render the animation directly to a file
    from manimlib.cli import main
    import sys
    sys.argv = ['cyberterror.py', 'CyberTerrorTargets', '-o']
    main()
