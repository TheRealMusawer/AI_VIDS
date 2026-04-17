import subprocess
from pathlib import Path
import textwrap


def generate_video_for_theme(theme: str, script_text: str, output_path: Path):
    """
    CURRENTLY: simple black background + centered text using ffmpeg.
    LATER: replace this with local text-to-video (ModelScope, AnimateDiff, etc.).
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text = script_text.replace("\n", " | ")
    text = textwrap.shorten(text, width=140, placeholder="...")

    drawtext = (
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='{text}':"
        "fontcolor=white:fontsize=48:"
        "x=(w-text_w)/2:y=(h-text_h)/2"
    )

    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=1080x1920:d=20",
        "-vf", drawtext,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y",
        str(output_path),
    ]

    print("Running ffmpeg to generate placeholder video...")
    subprocess.run(cmd, check=True)
    print(f"Video generated at {output_path}")
