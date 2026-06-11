import subprocess
import shutil
import os

skill_dir = r"e:\image_tool\claude-skill-aso-appstore-screenshots"
final_dir = r"e:\image_tool\screenshots\final"
artifact_dir = r"C:\Users\KIIT0001\.gemini\antigravity-ide\brain\6ef26848-c419-48c8-b6ad-ca25856b5eee"

# Ensure directories exist
os.makedirs(final_dir, exist_ok=True)
os.makedirs(artifact_dir, exist_ok=True)

configs = [
    {
        "verb": "IMAGE RESIZER",
        "desc": "",
        "subtitle": "Compress • Resize • Convert",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\home.jpg",
        "output": os.path.join(final_dir, "01-home.png"),
        "bg_start": "#1DD18A",
        "bg_end": "#00B96B",
        "glow_color": "#68FFB7",
        "verb_size": 150, # Slightly scaled to guarantee single line fits nicely
        "subtitle_size": 80
    },
    {
        "verb": "COMPRESS",
        "desc": "UP TO 90%",
        "subtitle": "SMALLER FILES",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\compress.jpg",
        "output": os.path.join(final_dir, "02-compress.png"),
        "bg_start": "#1DD18A",
        "bg_end": "#00B96B",
        "glow_color": "#68FFB7",
        "verb_size": 190,
        "subtitle_size": 80
    },
    {
        "verb": "CONVERT",
        "desc": "",
        "subtitle": "JPG ↔ PNG ↔ WEBP ↔ HEIC",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\convert.jpg",
        "output": os.path.join(final_dir, "03-convert.png"),
        "bg_start": "#9B5DFF",
        "bg_end": "#6F38FF",
        "glow_color": "#D0B3FF",
        "verb_size": 160,
        "subtitle_size": 80 # Made smaller for elegant spacing
    },
    {
        "verb": "RESIZE",
        "desc": "",
        "subtitle": "Custom dimensions in seconds",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\resize.jpg",
        "output": os.path.join(final_dir, "04-resize.png"),
        "bg_start": "#3D8DFF",
        "bg_end": "#1F6FFF",
        "glow_color": "#99C7FF",
        "verb_size": 160,
        "subtitle_size": 80
    },
    {
        "verb": "BATCH",
        "desc": "",
        "subtitle": "Process 4, 40 or 400 images",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\batch.jpg",
        "output": os.path.join(final_dir, "05-batch.png"),
        "bg_start": "#FF7E40",
        "bg_end": "#E64A19",
        "glow_color": "#FFC2A6",
        "verb_size": 160,
        "subtitle_size": 80
    },
    {
        "verb": "HISTORY",
        "desc": "",
        "subtitle": "Revisit previous exports anytime",
        "screenshot": r"e:\image_tool\assets\raw-screenshots\history.jpg",
        "output": os.path.join(final_dir, "06-history.png"),
        "bg_start": "#00D2C4",
        "bg_end": "#009688",
        "glow_color": "#A6FCFF",
        "verb_size": 160,
        "subtitle_size": 80
    }
]

print("Starting generation...")
for i, config in enumerate(configs):
    cmd = [
        "python",
        os.path.join(skill_dir, "compose.py"),
        "--bg_start", config["bg_start"],
        "--bg_end", config["bg_end"],
        "--verb", config["verb"],
        "--desc", config["desc"],
        "--subtitle", config["subtitle"],
        "--screenshot", config["screenshot"],
        "--output", config["output"],
        "--verb_size", str(config["verb_size"]),
        "--subtitle_size", str(config["subtitle_size"]),
        "--glow_color", config["glow_color"]
    ]
    print(f"Generating screenshot {i+1}: {config['verb']}")
    subprocess.run(cmd, check=True)

# Run showcase script without --github URL to prevent clutter
print("Generating showcase...")
showcase_cmd = [
    "python",
    os.path.join(skill_dir, "showcase.py"),
    "--screenshots",
    os.path.join(final_dir, "01-home.png"),
    os.path.join(final_dir, "02-compress.png"),
    os.path.join(final_dir, "03-convert.png"),
    os.path.join(final_dir, "04-resize.png"),
    os.path.join(final_dir, "05-batch.png"),
    os.path.join(final_dir, "06-history.png"),
    "--output", r"e:\image_tool\screenshots\showcase.png"
]
subprocess.run(showcase_cmd, check=True)

# Copy to artifacts directory
print("Copying final screens to artifacts directory...")
for config in configs:
    basename = os.path.basename(config["output"])
    dest = os.path.join(artifact_dir, basename)
    shutil.copy2(config["output"], dest)
    print(f"Copied {basename} to artifacts")

# Copy showcase to artifacts
shutil.copy2(r"e:\image_tool\screenshots\showcase.png", os.path.join(artifact_dir, "showcase.png"))
print("Copied showcase to artifacts")

print("All screenshots generated and copied successfully!")
