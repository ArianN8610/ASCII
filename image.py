from PIL import Image as Img


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
