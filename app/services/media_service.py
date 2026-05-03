from PIL import Image, ImageDraw
import cv2


class MediaService:
    def edit_image(self, input_path: str, output_path: str, text: str | None = None) -> str:
        img = Image.open(input_path).convert("RGB")
        w, h = img.size
        crop = img.crop((0, 0, int(w * 0.9), int(h * 0.9)))
        if text:
            draw = ImageDraw.Draw(crop)
            draw.text((20, 20), text, fill=(255, 255, 255))
        crop.save(output_path)
        return output_path

    def add_subtitles_to_video(self, input_path: str, output_path: str, subtitle_text: str) -> str:
        cap = cv2.VideoCapture(input_path)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.putText(frame, subtitle_text, (40, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(frame)

        cap.release()
        out.release()
        return output_path
