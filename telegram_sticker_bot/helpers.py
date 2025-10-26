from PIL import Image
import io


def chunkify(lst, size):
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def webp_to_png(webp_bytes: bytearray) -> bytes:
    image = Image.open(io.BytesIO(webp_bytes))
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output
