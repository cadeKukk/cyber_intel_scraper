#!/usr/bin/env python3
import os
import subprocess

# Activate the virtual environment and run the animation
cmd = [
    "source", "/Users/cadekukk/Documents/manim_projects/manim_env_311/bin/activate", 
    "&&", "manimgl", "simple_terror.py", "CyberTerrorismScene", "-o"
]

# Join the command for shell=True
cmd_str = " ".join(cmd)

# Run the command
print(f"Running: {cmd_str}")
result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)

# Print output
print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

print(f"Return code: {result.returncode}") 