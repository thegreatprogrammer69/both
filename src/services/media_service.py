from PIL import Image, ImageDraw
import cv2
import subprocess


class MediaService:
    async def edit_image(self, input_path: str, output_path: str, text: str | None = None) -> str:
        img = Image.open(input_path).convert("RGB")
        # MVP: имитация удаления людей с фона (blur)
        img = img.resize((img.width, img.height))
        if text:
            draw = ImageDraw.Draw(img)
            draw.text((20, 20), text, fill=(255, 255, 255))
        img.save(output_path)
        return output_path

    async def generate_images(self, prompt: str, count: int = 1) -> list[str]:
        # Заглушка под SD/API
        out = []
        for i in range(count):
            path = f"generated_{i}.png"
            Image.new("RGB", (1024, 1024), color=(20, 20, 20)).save(path)
            out.append(path)
        return out

    async def add_subtitles_to_video(self, input_path: str, subtitles_srt: str, output_path: str) -> str:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-vf", f"subtitles={subtitles_srt}", output_path,
        ], check=False)
        return output_path
