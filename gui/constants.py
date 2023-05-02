from os import getcwd
from os.path import join

""" GUI CONSTANTS """
FRAME_MIN_WIDTH = 275
FRAME_MIN_HEIGHT = 200

""" THEME CONSTANTS """

BUTTON_STYLE = "ttk.Button.CustomButton.TButton"
IMG_BUTTON_STYLE = "ttk.Button.ImgCustomButton.TButton"
LABEL_STYLE = "ttk.Label.CustomLabel.TLabel"

BLACKLIST_PRIMARY = "black"
BLACKLIST_SECONDARY = "white"

WHITELIST_PRIMARY = "white"
WHITELIST_SECONDARY = "black"

WIN_BG = "black"

FRAME_DARK_PRIMARY = "black"
FRAME_LIGHT_PRIMARY = "white"
FRAME_DARK_SECONDARY = "black"
FRAME_LIGHT_SECONDARY = "white"

IMG_BUTTON_LIGHT_PRIMARY = "white"
IMG_BUTTON_LIGHT_SECONDARY = "black"
IMG_BUTTON_DARK_PRIMARY = "black"
IMG_BUTTON_DARK_SECONDARY = "black"

BUTTON_LIGHT_PRIMARY = "white"
BUTTON_LIGHT_SECONDARY = "black"
BUTTON_DARK_PRIMARY = "black"
BUTTON_DARK_SECONDARY = "white"

LABEL_LIGHT_PRIMARY = "white"
LABEL_LIGHT_SECONDARY = "black"
LABEL_DARK_PRIMARY = "black"
LABEL_DARK_SECONDARY = "white"

""" ASSET PATH CONSTANTS"""
CWD = getcwd()
ASSETS_PATH = join(CWD, "gui", "assets")

LOGO_PATH = join(ASSETS_PATH, "logo.png")
PROFILE_PATH = join(ASSETS_PATH, "profile_icon.png")
SETTINGS_PATH = join(ASSETS_PATH, "settings_icon.png")
TITLE_PATH = join(ASSETS_PATH, "title_icon.png")
INFO_ICON_PATH = join(ASSETS_PATH, "info_icon.png")
SCAN_ICON_PATH = join(ASSETS_PATH, "scan_icon.png")
COLLECT_ICON_PATH = join(ASSETS_PATH, "collect_icon.png")
UPLOAD_ICON_PATH = join(ASSETS_PATH, "upload_icon.png")
SCAN_BUTTON_PATH = join(ASSETS_PATH, "scan_button.png")
COLLECT_BUTTON_PATH = join(ASSETS_PATH, "collect_button.png")
UPLOAD_BUTTON_PATH = join(ASSETS_PATH, "upload_button.png")
LIGHT_MODE_ICON = join(ASSETS_PATH, "light_mode.png")
DARK_MODE_ICON = join(ASSETS_PATH, "dark_mode.png")
EXPAND_OUTPUT_ICON_PATH = join(ASSETS_PATH, "expand_output.png")
COLLAPSE_OUTPUT_ICON_PATH = join(ASSETS_PATH, "collapse_output.png")

""" MISC. CONSTANTS """

about_text = """
        Instructions -
        scan systems: Performs a light weight scan on your 
        systems with the help of the Nmap library. Once complete,
        a list containing all devices on your systems will
        be displayed on this right-hand display.

        collect data: Performs an in-depth scan of your systems
        that allows it to collect information on each devices ports
        including: protocol, availability, and service. At this point
        you may also blacklist specific devices by clicking on 
        the devices name, then selecting the 'Add to blacklist' button.
        You may also remove that device from your blacklist by
        selecting the 'Remove from blacklist' button.

        upload data: Connects to our database server and updates
        the collected data to remove devices in the blacklist. Once
        complete, a message will appear stating whether your data
        was successfully uploaded or not.
        """

default_width, default_height = 800, 600
default_res = default_width, default_height
default_geometry = str(default_width) + 'x' + str(default_height)
default_text_size = 18
default_font = "Helvetica"
padding = (3, 3, 12, 12)
