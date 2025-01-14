from PIL import Image
import customtkinter as ctk
from utils import generator

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')
appWidth, appHeight = 1000, 500


def validator(self) -> float | None:
    """Validate values and return scale value"""

    if self.image_pathname is not None:
        image_width, image_height = Image.open(self.image_pathname).size
    else:
        self.message_label.configure(text='Image must be selected', text_color='red')
        return None

    # Get given values
    user_scale = self.scale_entry.get()
    user_width = self.width_entry.get()
    user_height = self.height_entry.get()

    if not user_scale and not user_width and not user_height:
        final_scale = 1  # If values aren't present, keep the image size constant
    elif (user_scale and user_width) or (user_scale and user_height) or (user_width and user_height):
        self.message_label.configure(text='Values for image size cannot be used at the same time',
                                     text_color='red')
        return None
    else:
        try:
            if user_scale:
                final_scale = float(user_scale) / 100
            elif user_width:
                final_scale = int(user_width) / image_width
            elif user_height:
                final_scale = int(user_height) / image_height
            else:
                self.message_label.configure(text='One of the scale, width and height values must be entered',
                                             text_color='red')
                return None
        except ValueError:
            self.message_label.configure(text='Enter number for scale, width or height', text_color='red')
            return None

    if self.txt_file_checkbox._check_state and not self.txt_folder_pathname:
        self.message_label.configure(text='Path of .txt file must be specified', text_color='red')
        return None

    if self.output_image_checkbox._check_state and not self.output_folder_pathname:
        self.message_label.configure(text='Path of output image must be specified', text_color='red')
        return None

    return final_scale


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure window
        self.title('ASCII')
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(False, False)

        # Set variables
        self.image_pathname = None
        self.txt_folder_pathname = None
        self.output_folder_pathname = None
        self.bg_color = 'Black'

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Main text
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ASCII Generator",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Dark mode option
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                             values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Image path and text file
        self.files_frame = ctk.CTkFrame(self)
        self.files_frame.grid(row=0, column=1, pady=(40, 0), padx=(20, 0), sticky="nsew")
        # Image
        self.select_img_button = ctk.CTkButton(master=self.files_frame, text='Select Image',
                                               command=self.select_file_event)
        self.select_img_button.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.display_img_path = ctk.CTkLabel(self.files_frame, text='')
        self.display_img_path.grid(row=0, column=1, padx=(15, 0), pady=(20, 0), sticky="w")
        # Text file
        self.txt_file_checkbox = ctk.CTkCheckBox(master=self.files_frame, text='Save .txt file',
                                                 command=self.txt_file_checkbox_event)
        self.txt_file_checkbox.grid(row=1, column=0, pady=(15, 0), padx=(20, 0), sticky="w")
        self.select_folder_button = ctk.CTkButton(master=self.files_frame, text='Select Folder',
                                                  command=lambda: self.select_folder_event('txt'))
        self.display_folder_path = ctk.CTkLabel(self.files_frame, text='')

        # Output image frame
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=1, column=1, pady=(20, 0), padx=(20, 0), sticky="nsew")
        # Output image checkbox
        self.output_image_checkbox = ctk.CTkCheckBox(master=self.image_frame, text='Save .png file',
                                                     command=self.output_image_checkbox_event)
        self.output_image_checkbox.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")
        # Output image button
        self.select_output_button = ctk.CTkButton(master=self.image_frame, text='Select Folder',
                                                  command=lambda: self.select_folder_event('img'))
        self.select_output_button.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.display_output_path = ctk.CTkLabel(self.image_frame, text='')
        self.display_output_path.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        # Background color
        self.background_color_label = ctk.CTkLabel(self.image_frame, text="Background Color:")
        self.background_color_label.grid(row=2, column=0, padx=(13, 0), pady=(10, 0), sticky="w")
        self.bg_color_option_menu = ctk.CTkOptionMenu(self.image_frame, values=['Black', 'White'],
                                                      command=self.change_bg_color_option_event)
        self.bg_color_option_menu.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))

        # Messages box
        self.message_label = ctk.CTkLabel(self, text='')
        self.message_label.grid(row=2, column=1)

        # Create chars entry and button
        self.chars = ctk.CTkEntry(self, placeholder_text="Characters")
        self.chars.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.create_button = ctk.CTkButton(master=self, fg_color="transparent", border_width=2,
                                           text_color=("gray10", "#DCE4EE"), text='Create',
                                           command=self.create_button_event)
        self.create_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=200, height=100)
        self.tabview.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Scale")
        self.tabview.add("Width")
        self.tabview.add("Height")
        self.tabview.tab("Scale").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Width").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Height").grid_columnconfigure(0, weight=1)
        # Scale Page
        ctk.CTkLabel(self.tabview.tab("Scale"), text='%').grid(row=0, column=0, padx=(160, 0), pady=(20, 10))
        self.scale_entry = ctk.CTkEntry(self.tabview.tab("Scale"), placeholder_text='Result Scale')
        self.scale_entry.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Width Page
        ctk.CTkLabel(self.tabview.tab("Width"), text='px').grid(row=0, column=0, padx=(160, 0), pady=(15, 10))
        self.width_entry = ctk.CTkEntry(self.tabview.tab("Width"), placeholder_text='Result Width')
        self.width_entry.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Height Page
        ctk.CTkLabel(self.tabview.tab("Height"), text='px').grid(row=0, column=0, padx=(160, 0), pady=(15, 10))
        self.height_entry = ctk.CTkEntry(self.tabview.tab("Height"), placeholder_text='Result Height')
        self.height_entry.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Warning text for all pages
        ctk.CTkLabel(self.tabview, text='Scale, width and Height\ncannot be used at the same time',
                     font=ctk.CTkFont(size=12, weight="bold")).grid(row=3, column=0, pady=(50, 0))

        # Create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.reverse_chars_checkbox = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text='Reverse characters',
                                                      command=self.reverse_chars_event)
        self.reverse_chars_checkbox.grid(row=1, column=0, pady=(40, 0), padx=(31, 0), sticky="n")
        self.copy_checkbox = ctk.CTkCheckBox(master=self.checkbox_slider_frame, text='Copy to clipboard')
        self.copy_checkbox.grid(row=2, column=0, pady=(20, 0), padx=(25, 0), sticky="n")

        # Set default values
        self.appearance_mode_optionemenu.set("System")
        self.chars.insert(0, 'Ñ@#W$9876543210?!abc;:+=-,._ ')
        self.select_output_button.configure(state='disabled')
        self.bg_color_option_menu.configure(state='disabled')

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_bg_color_option_event(self, bg_color: str):
        self.bg_color = bg_color

    def output_image_checkbox_event(self):
        if self.output_image_checkbox._check_state:
            self.select_output_button.configure(state='normal')
            self.bg_color_option_menu.configure(state='normal')
        else:
            self.select_output_button.configure(state='disabled')
            self.bg_color_option_menu.configure(state='disabled')

    def select_file_event(self):
        """Open window to select image"""

        filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        self.image_pathname = ctk.filedialog.askopenfilename(title='Select an image file', filetypes=filetypes)
        self.display_img_path.configure(
            text=self.image_pathname[:50] + '...' if len(self.image_pathname) > 50 else self.image_pathname)

    def txt_file_checkbox_event(self):
        if self.txt_file_checkbox._check_state:
            self.select_folder_button.grid(row=1, column=1, pady=(15, 0), padx=(5, 0), sticky="w")
            self.display_folder_path.grid(row=1, column=1, padx=(160, 0), pady=(15, 0), sticky="w")
        else:
            self.select_folder_button.grid_remove()
            self.display_folder_path.grid_remove()

    def select_folder_event(self, dir_type: str):
        """Open window to select a folder to save image or text"""

        if dir_type == 'txt':
            self.txt_folder_pathname = ctk.filedialog.askdirectory()
            self.display_folder_path.configure(
                text=self.txt_folder_pathname[:30] + '...' if len(
                    self.txt_folder_pathname) > 30 else self.txt_folder_pathname)
        else:
            self.output_folder_pathname = ctk.filedialog.askdirectory()
            self.display_output_path.configure(
                text=self.output_folder_pathname[:50] + '...' if len(
                    self.output_folder_pathname) > 50 else self.output_folder_pathname)

    def reverse_chars_event(self):
        chars = self.chars.get()
        self.chars.delete(0, 'end')
        self.chars.insert(0, chars[::-1])

    def create_button_event(self):
        final_scale = validator(self)
        if final_scale is not None:
            generator(self, final_scale)
            self.message_label.configure(text='Successfully done', text_color='green')
