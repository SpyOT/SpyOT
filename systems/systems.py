from cryptography.fernet import Fernet
from os import system

KEY = Fernet.generate_key()
fernet = Fernet(KEY)


class Systems:
    def __init__(self, env):
        self.env = env
        self.is_prod = self.env == 'prod'
        self.show_log = not self.is_prod
        utils.setup_local_storage(self.show_log)

        self.network_mgr = NetworkMgr()

    def scan(self):
        utils.print_log("Scanning network...", self.show_log)
        success = self.network_mgr.scan_network()
        utils.output_log(success,
                         src_succ="Scan complete",
                         src_err="Scan failed",
                         show=self.show_log)

    def collect(self):
        utils.print_log("Collecting data...", self.show_log)
        success = self.network_mgr.collect_data()
        utils.output_log(success,
                         src_succ="Collection complete",
                         src_err="Collection failed",
                         show=self.show_log)

    def update_device_blacklist_status(self, ip, value):
        utils.print_log(f"Updating blacklist status {ip}...", self.show_log)
        success = self.network_mgr.set_blacklist_status(ip, value)
        utils.output_log(success,
                         src_succ="Blacklist status updated",
                         src_err="Blacklist status update failed",
                         show=self.show_log)

    def view_report(self):
        report_path = self.network_mgr.report_path
        utils.print_log(f"Viewing report {report_path}...", self.show_log)
        # Open report in notepad
        system(f"notepad {report_path}")

    def get_metadata(self):
        return self.network_mgr.get_metadata()

    def get_hostname(self):
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return metadata.loc[metadata['type'] == 'router', ['name']].values[0][0]
        else:
            return ""

    def get_devices(self):
        # Get list of devices from metadata
        metadata = self.network_mgr.get_metadata()
        if not metadata.empty:
            return [name[0] for name in metadata.loc[metadata['type'] == 'device', ['name']].values]
        else:
            return []


def main():

    systems = Systems('dev')
    systems.scan()
    device_ip = systems.network_mgr.get_device_ips()[0]
    systems.update_device_blacklist_status(device_ip, True)
    systems.collect()
    # systems.view_report()


if __name__ == '__main__':
    from networkmgr import NetworkMgr
    import utils
    main()
else:
    from .networkmgr import NetworkMgr
    from . import utils

