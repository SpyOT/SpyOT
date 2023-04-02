# Constants
default_width, default_height = 800, 600
default_res = default_width, default_height
default_geometry = str(default_width) + 'x' + str(default_height)
default_text_size = 18
default_font = "Helvetica"
padding = (3, 3, 12, 12)
asset_path = "gui/assets/"
logo_img = asset_path + "logo.png"
profile_path = asset_path + "profile_icon.png"
setting_path = asset_path + "settings_icon.png"
title_path = asset_path + "title_icon.png"
info_path = asset_path + "info_icon.png"
scan_path = asset_path + "scan_icon.png"
collect_path = asset_path + "collect_icon.png"
upload_path = asset_path + "transfer_icon.png"
exit_path = asset_path + "exit_icon.png"
scan_button = asset_path + "scan_button.png"
collect_button = asset_path + "collect_button.png"
upload_button = asset_path + "upload_button.png"
expand_button = asset_path + "expand_output.png"
collapse_button = asset_path + "collapse_output.png"
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
