import pyperclip
from image import Image
from pathlib import Path
from datetime import datetime


def save_txt_file(txt_path: Path, text: str):
    """Save ASCII text file"""

    file_name = f'ascii image {datetime.now().strftime("%Y-%m-%d %H%M%S")}.txt'
    path_file = txt_path / file_name
    with open(path_file, 'w', encoding='utf-8') as f:
        f.write(text)


def generator(self, scale: float):
    chars = self.chars.get()
    image = Image(self.image_pathname, scale)

    if self.txt_file_checkbox._check_state or self.copy_checkbox._check_state:
        ascii_image = image.convert_to_ascii(chars)

    if self.txt_file_checkbox._check_state:
        txt_folder_path = Path(self.txt_folder_pathname)
        save_txt_file(txt_folder_path, ascii_image)

    if self.copy_checkbox._check_state:
        pyperclip.copy(ascii_image)

    if self.output_image_checkbox._check_state:
        image.create_ascii_image(Path(self.output_folder_pathname), chars, self.bg_color.lower())
