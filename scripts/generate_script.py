import subprocess
import json
import tempfile
from pathlib import Path

MODEL_PATH = "models/llm/phi-2.gguf"  # you will download this in the workflow

def generate_script_for_theme(theme: str):
    prompt = f"""
Write a 3-sentence YouTube Shorts script about this theme: {theme}.
Keep it punchy, interesting, and under 40 words total.
"""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(prompt.encode("utf-8"))
        tmp_path = tmp.name

    result = subprocess.run(
        [
            "./llama.cpp/main",
            "-m", MODEL_PATH,
            "-p", prompt,
            "-n", "120"
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    title = f"{theme} #{abs(hash(output)) % 9999}"

    return output, title
