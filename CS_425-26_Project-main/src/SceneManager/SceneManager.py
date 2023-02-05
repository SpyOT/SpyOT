import src.SceneManager.scenes as scene
from tkinter import ttk
import src.SceneManager.constants as preset

class SceneManager:
    def __init__(self, root):
        self.root = root
        self.configure_root()
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.scenes = {
            "title": scene.TitleScreen(self),
            "home": scene.Home(self),
            "security": scene.Security(self),
            "settings": scene.Settings(self)
        }
        self.scene = None
        self.current_scene("title")

    def current_scene(self, scene_name):
        self.scene = self.scenes[scene_name]
        self.scene.display_content()

    def change_scene(self, new_scene):
        self.scene.remove_content()
        self.current_scene(new_scene)

    def configure_root(self):
        self.root.geometry(preset.default_geometry)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
