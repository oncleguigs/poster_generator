

import base64
from io import BytesIO
from typing import BinaryIO

def convert_base64_to_file(base64_image: str) -> BinaryIO:
    base64_data = base64_image.split(",", 1)[-1] if "," in base64_image else base64_image
    image_bytes = base64.b64decode(base64_data)
    return BytesIO(image_bytes)
