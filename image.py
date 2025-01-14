from pathlib import Path
from datetime import datetime

from PIL import Image as Img, ImageDraw, ImageFont


class Image:
    def __init__(self, img_path: str, scale: float):
        self.image = Img.open(img_path)
        self.scale = scale

    @property
    def image_size(self) -> tuple:
        """Get new image size based on scale"""

        width, height = self.image.size  # Get the original size of the image

        width = int(width * self.scale) * 2
        height = int(height * self.scale)

        return width, height

    def resize_image(self):
        """Resize the image based on scale value"""
        return self.image.resize(self.image_size)  # Resize the image based on new dimensions

    def grayscale(self):
        """Change image color to grayscale"""
        return self.resize_image().convert('L')

    def convert_to_ascii(self, chars: str) -> str:
        """Create ASCII from image"""

        pixels = self.grayscale().load()  # Get image pixels
        width, height = self.image_size

        # Create ASCII
        rows = []
        for y in range(height):
            row = ''
            for x in range(width):
                row += chars[((pixels[x, y] * len(chars)) // 255) - 1]
            rows.append(row)

        return '\n'.join(rows)

    def create_ascii_image(self, image_path: Path, chars: str, background_color: str):
        """Create an image from ASCII"""

        one_char_width = 8  # Width of each character in image
        one_char_height = 18  # Height of each character in image
        font = ImageFont.truetype('arial.ttf', 15)
        pixels = self.resize_image().load()  # Get image pixels
        width, height = self.image_size
        output_image = Img.new('RGB', (one_char_width * width, one_char_height * height),
                               color=background_color)  # Create an empty image frame with image and char size
        d = ImageDraw.Draw(output_image)

        # Draw ASCII characters to the image frame
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                h = int(r/3 + g/3 + b/3)
                char = chars[((h * len(chars)) // 255) - 1]
                d.text((x * one_char_width, y * one_char_height), char, font=font, fill=(r, g, b))

        output_image.save(image_path / f'ascii image {datetime.now().strftime("%Y-%m-%d %H%M%S")}.png')  # Save image
