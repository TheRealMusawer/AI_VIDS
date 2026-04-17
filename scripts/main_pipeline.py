import json
from pathlib import Path

from generate_script import generate_script_for_theme
from generate_video import generate_video_for_theme
from upload_to_youtube import upload_short
from delete_old_videos import delete_previous_batch

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

THEMES_PATH = CONFIG_DIR / "themes.json"
SETTINGS_PATH = CONFIG_DIR / "settings.json"


def load_config():
    with open(THEMES_PATH, "r", encoding="utf-8") as f:
        themes = json.load(f)["themes"]
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)
    return themes, settings


def main():
    themes, settings = load_config()

    if settings.get("delete_previous_batch", True):
        print("Deleting previous batch of videos...")
        delete_previous_batch(count=len(themes))

    uploaded_ids = []

    for idx, theme in enumerate(themes, start=1):
        print(f"\n=== [{idx}/{len(themes)}] Theme: {theme} ===")

        script_text, title = generate_script_for_theme(theme)
        print("Script preview:", script_text[:120].replace("\n", " ") + "...")

        video_path = OUTPUT_DIR / f"short_{idx}.mp4"
        generate_video_for_theme(theme, script_text, video_path)

        vid_id = upload_short(
            video_file=str(video_path),
            title=title,
            description=f"Auto-generated short about: {theme}",
            tags=[theme.replace(" ", ""), "AI", "Shorts"],
        )
        uploaded_ids.append(vid_id)
        print(f"Uploaded video ID: {vid_id}")

    print("\nAll shorts done.")
    print("Video IDs:", uploaded_ids)


if __name__ == "__main__":
    main()
