# Javier Perez
# SpyOT user network scan unit test
# 03/03/23
# networkScanUnitTest.py

from ..main import TestMain
import unittest


class testSpyOT(unittest.TestCase):
    def test_network_config_button(self):
        app_test = TestMain()
        title_screen = app_test.curr_scene
        curr_scene = title_screen.current_scene
        curr_scene.create_profile_button.invoke()
        curr_scene = title_screen.current_scene
        before_scan = curr_scene.network_found
        curr_scene.configure_button.invoke()
        after_scan = curr_scene.network_found
        curr_scene.exit_button.invoke()
        curr_scene = title_screen.current_scene
        curr_scene.exit_button.invoke()
        self.assertNotEqual(before_scan, after_scan)


if __name__ == '__main__':
    unittest.main()