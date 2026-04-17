import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# NEW llama.cpp binary path (CMake build)
LLAMA_BIN = BASE_DIR / "llama.cpp" / "build" / "bin" / "llama-cli"

# Local model path
MODEL_PATH = BASE_DIR / "models" / "llm" / "tiny-llm.gguf"


def generate_script_for_theme(theme: str):
    prompt = f"""
You are writing a YouTube Shorts script.

Theme: {theme}

Write 3 short sentences, total under 40 words.
Make it punchy, engaging, and easy to read as on-screen text.
Do NOT add titles, labels, or extra commentary. Just the 3 sentences.
"""

    if not LLAMA_BIN.exists():
        raise RuntimeError(f"llama.cpp binary not found at: {LLAMA_BIN}")

    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found at: {MODEL_PATH}")

    # Run llama.cpp
    result = subprocess.run(
        [
            str(LLAMA_BIN),
            "-m", str(MODEL_PATH),
            "-p", prompt,
            "-n", "120",
            "--temp", "0.8"
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    # Clean output: take last 3 lines
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    script_text = "\n".join(lines[-3:]) if len(lines) >= 3 else "\n".join(lines)

    title = f"{theme} #{abs(hash(script_text)) % 9999}"

    return script_text, title
