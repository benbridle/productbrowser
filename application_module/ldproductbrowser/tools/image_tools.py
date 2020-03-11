"""
Helper functions for working with PIL images
"""

import io
from PIL import Image
import PIL


def convert_bytes_to_pil_image(image_bytes):
    """
    Convert a bytes object to a PIL image.
    """
    if not isinstance(image_bytes, bytes):
        raise TypeError("Image must be a bytes object")
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except PIL.UnidentifiedImageError:
        raise ValueError("Bytes object does not contain an image")
    return image


def convert_pil_image_to_bytes(image):
    """
    Convert a PIL image to a bytes object.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("Image must be a PIL image")
    image_bytes = io.BytesIO()
    try:
        image.save(image_bytes, format="PNG")
    except OSError:
        image.save(image_bytes, format="JPEG")
    image_bytes = image_bytes.getvalue()
    return image_bytes


def scale_image(image: Image, width, height):
    """
    Scale the image to fit the given size, preserving aspect ratio.
    """
    image.thumbnail((width, height), Image.ANTIALIAS)
    return image


def superimpose_image_on_background(image: Image, width, height, colour=(255, 255, 255, 0)):
    """
    Scales the image to fit the given size while preserving aspect ratio,
    and superimposes the result over the center of a coloured background of
    the given size.
    """
    image = scale_image(image, width, height)
    im_width, im_height = image.size
    background = Image.new("RGBA", (width, height), colour)
    offset = ((width - im_width) // 2, (height - im_height) // 2)
    background.paste(image, offset)
    return background
