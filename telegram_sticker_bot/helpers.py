import os
from PIL import Image
import io
import ffmpeg
import tempfile


def chunkify(lst, size):
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def webp_to_bytes(webp_bytes: bytearray, format: str = "PNG") -> bytes:
    image = Image.open(io.BytesIO(webp_bytes))
    output = io.BytesIO()
    image.save(output, format=format)
    output.seek(0)
    return output


def convert_webm_bytes_to_mp4_bytes(input_bytes: bytearray) -> bytes | None:
    mp4_data = None

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_in:
        temp_in.write(input_bytes)
        temp_in_path = temp_in.name

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_out:
        temp_out_path = temp_out.name

    try:
        (
            ffmpeg.input(temp_in_path)
            .filter("scale", w="trunc(iw/2)*2", h="trunc(ih/2)*2")
            .output(temp_out_path, vcodec="libx264", acodec="aac")
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )

        with open(temp_out_path, "rb") as f:
            mp4_data = f.read()

        print("✅ Conversion successful")

    except ffmpeg.Error as e:
        print("❌ FFmpeg Conversion Error:")
        print(e.stderr.decode("utf8"))

    finally:
        if os.path.exists(temp_in_path):
            os.unlink(temp_in_path)
        if os.path.exists(temp_out_path):
            os.unlink(temp_out_path)

    return mp4_data
