from diffusers import DiffusionPipeline
import torch
from pathlib import Path

def generate_video_for_theme(theme, script_text, output_path):
    output_path = Path(output_path)

    pipe = DiffusionPipeline.from_pretrained(
        "damo-vilab/text-to-video-ms-1.7b",
        torch_dtype=torch.float32
    )

    pipe.enable_model_cpu_offload()

    video_frames = pipe(script_text, num_frames=16).frames

    # Save as mp4
    import imageio
    imageio.mimsave(output_path, video_frames, fps=8)
