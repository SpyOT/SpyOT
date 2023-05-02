from .custom_widgets import CustomContainer, CustomButton, CustomLabel
from tkinter import PhotoImage
from gui import constants as const

const.BUTTON_STYLE = const.IMG_BUTTON_STYLE


class MainView(CustomContainer):
    def __init__(self, frame, systems, **kwargs):
        super().__init__(
            frame,
            systems,
            **kwargs)
        self.configure_win(col_config={'col 0': 'weight 1',
                                       'col 1': 'weight 1',
                                       'col 2': 'weight 1',
                                       'col 3': 'weight 1'},
                           row_config={'row 0': 'weight 1',
                                       'row 1': 'weight 1',
                                       'row 2': 'weight 1',
                                       'row 3': 'weight 1',
                                       'row 4': 'weight 1'})
        self.toggle_icon = None

    def set_toggle_icon(self, icon):
        self.toggle_icon = icon
        self.display_frame()

    def set_widgets(self, controller):
        """ Sets all widgets for the main view"""

        """ Header widgets """
        profile_icon = PhotoImage(file=const.PROFILE_PATH)
        self.set_widget("profile", CustomButton,
                        image=profile_icon,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("profile"))

        title_icon = PhotoImage(file=const.TITLE_DARK_PATH)
        self.set_widget("title", CustomLabel,
                        image=title_icon,
                        style='ttk.Label.CustomLabel.TLabel')
        settings_icon = PhotoImage(file=const.SETTINGS_PATH)
        self.set_widget("settings", CustomButton,
                        image=settings_icon,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("settings"))

        """ Body widgets """
        # scan icon and button
        scan_icon = PhotoImage(file=const.SCAN_ICON_PATH)
        self.set_widget("scan_icon", CustomLabel,
                        image=scan_icon,
                        style='ttk.Label.CustomLabel.TLabel')
        scan_button = PhotoImage(file=const.SCAN_BUTTON_PATH)
        self.set_widget("scan_btn", CustomButton,
                        image=scan_button,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("output_scan"))

        # collect icon and button
        collect_icon = PhotoImage(file=const.COLLECT_ICON_PATH)
        self.set_widget("collect_icon", CustomLabel,
                        image=collect_icon,
                        style='ttk.Label.CustomLabel.TLabel')
        collect_button = PhotoImage(file=const.COLLECT_BUTTON_PATH)
        self.set_widget("collect_btn", CustomButton,
                        image=collect_button,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("collect"))

        # upload icon and button
        upload_icon = PhotoImage(file=const.UPLOAD_ICON_PATH)
        self.set_widget("upload_icon", CustomLabel,
                        image=upload_icon,
                        style='ttk.Label.CustomLabel.TLabel')
        upload_button = PhotoImage(file=const.UPLOAD_BUTTON_PATH)
        self.set_widget("upload_btn", CustomButton,
                        image=upload_button,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("upload"))

        """ Footer widgets """
        info_icon = PhotoImage(file=const.INFO_ICON_PATH)
        self.set_widget("info_icon", CustomButton,
                        image=info_icon,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("info"))
        expand_output_icon = PhotoImage(file=const.EXPAND_OUTPUT_ICON_PATH)
        self.set_widget("expand_output_icon", CustomButton,
                        image=expand_output_icon,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("toggle_output"))
        collapse_output_icon = PhotoImage(file=const.COLLAPSE_OUTPUT_ICON_PATH)
        self.set_widget("collapse_output_icon", CustomButton,
                        image=collapse_output_icon,
                        style=const.BUTTON_STYLE,
                        command=lambda: controller.handle_btn_press("toggle_output"))
        self.toggle_icon = "expand"

    def display_widgets(self):
        """ Display Header Widgets """
        self.display_widget("profile", sticky='nsew',
                            column=0, row=0,
                            padx=15, pady=15)
        self.display_widget("title", sticky='ns',
                            column=1, columnspan=2, row=0,
                            padx=15, pady=15)
        self.display_widget("settings", sticky='nsew',
                            column=3, row=0,
                            padx=15, pady=15)

        """ Display Body Widgets """
        self.display_widget("scan_icon", sticky='nsew',
                            column=0, row=1, columnspan=2,
                            padx=15, pady=15)
        self.display_widget("scan_btn", sticky='nsew',
                            column=2, row=1, columnspan=2,
                            padx=15, pady=15)
        self.display_widget("collect_icon", sticky='nsew',
                            column=0, row=2, columnspan=2,
                            padx=15, pady=15)
        self.display_widget("collect_btn", sticky='nsew',
                            column=2, row=2, columnspan=2,
                            padx=15, pady=15)
        self.display_widget("upload_icon", sticky='nsew',
                            column=0, row=3, columnspan=2,
                            padx=15, pady=15)
        self.display_widget("upload_btn", sticky='nsew',
                            column=2, row=3, columnspan=2,
                            padx=15, pady=15)

        """ Display Footer Widgets """
        self.display_widget("info_icon", sticky='nsew',
                            column=0, row=4,
                            padx=15, pady=15)
        if self.toggle_icon == "expand":
            self.display_widget("expand_output_icon", sticky='nsew',
                                column=3, row=4,
                                padx=15, pady=15)
        else:
            self.display_widget("collapse_output_icon", sticky='nsew',
                                column=3, row=4,
                                padx=15, pady=15)
