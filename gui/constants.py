from os import getcwd
from os.path import join

""" GUI CONSTANTS """
FRAME_MIN_WIDTH = 275
FRAME_MIN_HEIGHT = 200

""" THEME CONSTANTS """

BUTTON_STYLE = "ttk.Button.CustomButton.TButton"
IMG_BUTTON_STYLE = "ttk.Button.ImgCustomButton.TButton"
LABEL_STYLE = "ttk.Label.CustomLabel.TLabel"

DARK_BG_PRIMARY = "#1E313B"
LIGHT_BG_PRIMARY = "#F0EAD6"
LIGHT_BG_SECONDARY = "white"

BLACKLIST_PRIMARY = DARK_BG_PRIMARY
BLACKLIST_SECONDARY = LIGHT_BG_PRIMARY

WHITELIST_PRIMARY = LIGHT_BG_PRIMARY
WHITELIST_SECONDARY = DARK_BG_PRIMARY

WIN_BG = DARK_BG_PRIMARY

FRAME_DARK_PRIMARY = DARK_BG_PRIMARY
FRAME_LIGHT_PRIMARY = LIGHT_BG_PRIMARY
FRAME_DARK_SECONDARY = DARK_BG_PRIMARY
FRAME_LIGHT_SECONDARY = LIGHT_BG_PRIMARY

IMG_BUTTON_LIGHT_PRIMARY = LIGHT_BG_PRIMARY
IMG_BUTTON_LIGHT_SECONDARY = DARK_BG_PRIMARY
IMG_BUTTON_DARK_PRIMARY = DARK_BG_PRIMARY
IMG_BUTTON_DARK_SECONDARY = LIGHT_BG_SECONDARY

BUTTON_LIGHT_PRIMARY = LIGHT_BG_SECONDARY
BUTTON_LIGHT_SECONDARY = LIGHT_BG_SECONDARY
BUTTON_DARK_PRIMARY = LIGHT_BG_SECONDARY
BUTTON_DARK_SECONDARY = LIGHT_BG_SECONDARY

LABEL_LIGHT_PRIMARY = LIGHT_BG_PRIMARY
LABEL_LIGHT_SECONDARY = DARK_BG_PRIMARY
LABEL_DARK_PRIMARY = DARK_BG_PRIMARY
LABEL_DARK_SECONDARY = LIGHT_BG_PRIMARY

""" ASSET PATH CONSTANTS"""
CWD = getcwd()
ASSETS_PATH = join(CWD, "gui", "assets")

""" MainView ASSETS"""
LOGO_PATH = join(ASSETS_PATH, "logo.png")
PROFILE_PATH = join(ASSETS_PATH, "profile_icon.png")
SETTINGS_PATH = join(ASSETS_PATH, "settings_icon.png")
TITLE_PATH = join(ASSETS_PATH, "title_icon.png")
TITLE_DARK_PATH = join(ASSETS_PATH, "title_dark_icon.png")
INFO_ICON_PATH = join(ASSETS_PATH, "info_icon.png")
SCAN_ICON_PATH = join(ASSETS_PATH, "scan_icon.png")
COLLECT_ICON_PATH = join(ASSETS_PATH, "collect_icon.png")
UPLOAD_ICON_PATH = join(ASSETS_PATH, "upload_icon.png")
SCAN_BUTTON_PATH = join(ASSETS_PATH, "scan_button.png")
COLLECT_BUTTON_PATH = join(ASSETS_PATH, "collect_button.png")
UPLOAD_BUTTON_PATH = join(ASSETS_PATH, "upload_button.png")
EXPAND_OUTPUT_ICON_PATH = join(ASSETS_PATH, "expand_output.png")
COLLAPSE_OUTPUT_ICON_PATH = join(ASSETS_PATH, "collapse_output.png")

""" Settings ASSETS """
LIGHT_MODE_ICON = join(ASSETS_PATH, "light_mode.png")
DARK_MODE_ICON = join(ASSETS_PATH, "dark_mode.png")

""" Output ASSETS """
BLACKLIST_ICON_PATH = join(ASSETS_PATH, "blacklist_icon.png")
WHITELIST_ICON_PATH = join(ASSETS_PATH, "whitelist_icon.png")
CANCEL_ICON_PATH = join(ASSETS_PATH, "cancel_icon.png")
EDIT_LIST_ICON_PATH = join(ASSETS_PATH, "edit_list_icon.png")
LOGIN_ICON_PATH = join(ASSETS_PATH, "login_icon.png")
LOGOUT_ICON_PATH = join(ASSETS_PATH, "logout_icon.png")
NEW_SCAN_ICON_PATH = join(ASSETS_PATH, "new_scan_icon.png")
SAVE_REPORT_ICON_PATH = join(ASSETS_PATH, "save_report_icon.png")
VIEW_REPORT_ICON_PATH = join(ASSETS_PATH, "view_report_icon.png")
LOADING_ICON_PATH = join(ASSETS_PATH, "loading_icon.png")
LOADING_DARK_ICON_PATH = join(ASSETS_PATH, "loading_dark_icon.png")
EMAIL_LABEL = join(ASSETS_PATH, "email_label.png")
PASSWORD_LABEL = join(ASSETS_PATH, "password_label.png")
EMAIL_DARK_LABEL = join(ASSETS_PATH, "email_dark_label.png")
PASSWORD_DARK_LABEL = join(ASSETS_PATH, "password_dark_label.png")
LOGIN_PROMPT = join(ASSETS_PATH, "login_prompt.png")
LOGIN_DARK_PROMPT = join(ASSETS_PATH, "login_dark_prompt.png")
SCAN_LABEL = join(ASSETS_PATH, "scan_label.png")
SCAN_DARK_LABEL = join(ASSETS_PATH, "scan_dark_label.png")

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
