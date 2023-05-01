from datetime import datetime
from os import getcwd, listdir, mkdir, remove, system
from os.path import isfile, join, exists

# Constants
GEN_ERROR = 'Unknown error!'
CWD = getcwd()
if 'systems' in CWD:
    CWD = join(CWD, '..')
LOCAL_STORAGE_PATH = join(CWD, 'systems', 'local')
LOCAL_SCANS_PATH = join(LOCAL_STORAGE_PATH, 'scans')
LOCAL_REPORTS_PATH = join(LOCAL_STORAGE_PATH, 'reports')
BLACKLIST_PATH = join(LOCAL_STORAGE_PATH, 'blacklist.txt')
FILE_COUNT_LIMIT = 5
FILE_TIME_LIMIT = 5


# Utility Methods
def setup_local_storage(show_log):
    # Create 'local' directory
    create_dir(LOCAL_STORAGE_PATH, show_log)
    # Create 'scans' folder in 'local' directory
    create_dir(LOCAL_SCANS_PATH, show_log)
    # Create 'reports' folder in 'local' directory
    create_dir(LOCAL_REPORTS_PATH, show_log)


def create_dir(dir_path, show):
    try:
        mkdir(dir_path)
        action = ' '.join(['create directory', dir_path])
        print_success(action, show)
    except OSError:
        src = ' '.join(['dir exists', dir_path])
        print_error(src, show)
    except:
        src = ' '.join([GEN_ERROR, dir_path])
        print_error(src, show)


def create_file(file_path, show):
    if exists(file_path):
        action = ' '.join(['file exists', file_path])
        print_error(action, show)
    else:
        with open(file_path, 'w') as _:
            pass
        action = ' '.join(['create file', file_path])
        print_success(action, show)


def print_success(action, show):
    success_msg = ': '.join(['!Successful', action])
    if show:
        print(success_msg)


def print_error(src, show):
    error_msg = ': '.join(['!Error', src])
    if show:
        print(error_msg)


def output_log(condition, src_succ, src_err, show):
    if condition:
        print_success(src_succ, show)
    else:
        print_error(src_err, show)


def print_log(src, show):
    log_msg = ' '.join(['Started', src])
    if show:
        print(log_msg)


def get_recent_scan():
    if not exists(LOCAL_SCANS_PATH):
        return ""
    files = [f for f in listdir(LOCAL_SCANS_PATH) if isfile(join(LOCAL_SCANS_PATH, f))]
    if len(files) == 0:
        return ""
    return join(LOCAL_SCANS_PATH, max(files, key=lambda f: f.split('-')[1]))


def get_scan_path(scan_name):
    return join(LOCAL_SCANS_PATH, scan_name)


def new_scan_path():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    scan_name = '-'.join(['scan', timestamp + '.txt'])
    return join(LOCAL_SCANS_PATH, scan_name)


def clean_up_local_storage():
    print_log('cleaning up local storage', True)
    removed_scans = purge_old_files(LOCAL_SCANS_PATH,
                                    count_limit=FILE_COUNT_LIMIT,
                                    time_limit=FILE_TIME_LIMIT)
    removed_reports = purge_old_files(LOCAL_REPORTS_PATH,
                                      count_limit=FILE_COUNT_LIMIT,
                                      time_limit=FILE_TIME_LIMIT)
    print('removed ' + str(removed_scans) + ' scans and ' + str(removed_reports) + ' reports')


def purge_old_files(path, count_limit=10, time_limit=14):
    removed_files = 0
    path_files = listdir(path)
    # sort the files by date
    path_files.sort(key=lambda x: datetime.strptime(x.strip('.txt').strip('scan-').strip('report-'),
                                                    '%Y-%m-%d-%H-%M-%S'), reverse=True)
    if exists(path):
        for i, file in enumerate(path_files):
            # strip the file name of the extension and 'scan-' or 'report-'
            timestamp = file.strip('.txt').strip('scan-').strip('report-')
            # check how old the file is in days
            file_age = (datetime.now() - datetime.strptime(timestamp, '%Y-%m-%d-%H-%M-%S')).days
            # if file is older than time_limit days or
            # there are more than count_limit files
            # delete the file
            if file_age == time_limit or i >= count_limit:
                remove(join(path, file))
                removed_files += 1
    return removed_files


def new_report_path():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    report_name = '-'.join(['report', timestamp + '.txt'])
    return join(LOCAL_REPORTS_PATH, report_name)


def get_blacklist_ips():
    blacklist = []
    with open(BLACKLIST_PATH, 'r') as file:
        for device_ip in file:
            blacklist.append(device_ip.strip())
    return blacklist
