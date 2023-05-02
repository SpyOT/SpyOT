from os import system
from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
fernet = Fernet(KEY)


class Systems:
    def __init__(self, env):
        self.env = env
        self.is_prod = self.env == 'prod'
        self.show_log = not self.is_prod
        utils.setup_local_storage(self.show_log)

        self.network_mgr = NetworkMgr()
        self.firebase = FireBase()

    def scan(self):
        utils.print_log("Scanning network...", self.show_log)
        success = self.network_mgr.scan_network()
        utils.output_log(success,
                         src_succ="Scan complete",
                         src_err="Scan failed",
                         show=self.show_log)
        return success

    def collect(self):
        utils.print_log("Collecting data...", self.show_log)
        success = self.network_mgr.collect_data()
        utils.output_log(success,
                         src_succ="Collection complete",
                         src_err="Collection failed",
                         show=self.show_log)
        return success

    def upload(self):
        utils.print_log("Uploading data...", self.show_log)
        data = self.network_mgr.format_upload_data()
        try:
            assert(data is not None)
            success = self.firebase.upload_to_db(data)
            utils.output_log(success,
                             src_succ="Upload complete",
                             src_err="Upload failed",
                             show=self.show_log)
        except AssertionError:
            utils.print_error("No data to upload", self.show_log)
            success = False
        except Exception as e:
            utils.print_error(e, self.show_log)
            success = False
        return success

    def create_user(self, email, password):
        utils.print_log("Creating profile...", self.show_log)
        success = self.firebase.create_user(email, password)
        utils.output_log(success,
                         src_succ="Profile created",
                         src_err="Profile creation failed",
                         show=self.show_log)
        return success

    def signin_user(self, email, password):
        utils.print_log("Signing in...", self.show_log)
        success = self.firebase.signin_user(email, password)
        utils.output_log(success,
                         src_succ="Signed in",
                         src_err="Sign in failed",
                         show=self.show_log)
        return success

    def signout_user(self):
        utils.print_log("Signing out...", self.show_log)
        success = self.firebase.signout_user()
        utils.output_log(success,
                         src_succ="Signed out",
                         src_err="Sign out failed",
                         show=self.show_log)
        return success

    def refresh_session(self):
        utils.print_log("Refreshing session...", self.show_log)
        success = self.firebase.refresh_session()
        utils.output_log(success,
                         src_succ="Session refreshed",
                         src_err="Session refresh failed",
                         show=self.show_log)
        return success

    def is_logged_in(self):
        if self.firebase.get_user() is not None:
            self.refresh_session()
        return self.firebase.get_user() is not None

    def update_device_blacklist_status(self, ip, value):
        utils.print_log(f"Updating blacklist status {ip}...", self.show_log)
        success = self.network_mgr.set_blacklist_status(ip, value)
        utils.output_log(success,
                         src_succ="Blacklist status updated",
                         src_err="Blacklist status update failed",
                         show=self.show_log)
        return success

    def view_recent_report(self, report_path=''):
        if not report_path:
            report_path = self.network_mgr.report_path
        utils.print_log(f"Viewing report {report_path}...", self.show_log)
        # Open report in notepad
        system(f"notepad {report_path}")

    def metadata_available(self):
        return not self.network_mgr.get_metadata().empty

    def get_metadata(self):
        return self.network_mgr.get_metadata()

    def get_hostname(self):
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return self.network_mgr.get_hostname()
        else:
            return ""

    def get_devices(self):
        # Get list of devices from metadata
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return [name[0] for name in metadata.loc[metadata['type'] == 'device', ['name']].values]
        else:
            return []

    def get_device_metadata(self, name):
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return metadata.loc[metadata['name'] == name]
        else:
            return None

    def get_device_ip(self, name):
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return metadata.loc[metadata['name'] == name, ['ip']].values[0][0]
        else:
            return None

    def get_device_status(self, name):
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return metadata.loc[metadata['name'] == name, ['blacklist']].values[0][0]
        else:
            return None

    def get_device_summary(self):
        utils.print_log("Getting device summary...", self.show_log)
        ip_to_status = self.network_mgr.get_device_summary()
        device_summary = {ip: {'hostname': self.network_mgr.get_device_name(ip),
                               'status': ip_to_status[ip]}
                          for ip in ip_to_status}
        return device_summary


def main():
    systems = Systems('dev')
    systems.scan()
    device_ip = systems.network_mgr.get_device_ips()[0]
    systems.update_device_blacklist_status(device_ip, True)
    systems.collect()
    # systems.view_report()


if __name__ == '__main__':
    from networkmgr import NetworkMgr
    from firebase import FireBase
    import utils

    main()
else:
    from .networkmgr import NetworkMgr
    from .firebase import FireBase
    from . import utils
