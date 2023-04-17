from os import getcwd, listdir, mkdir, remove, system
from os.path import isfile, join, exists

# Constants
GEN_ERROR = 'Unknown error!'
CWD = getcwd()
LOCAL_STORAGE_PATH = join(CWD, 'systems', 'local')
LOCAL_SCANS_PATH = join(LOCAL_STORAGE_PATH, 'scans')
BLACKLIST_PATH = join(LOCAL_STORAGE_PATH, 'blacklist.txt')


# Utility Methods
def setup_local_storage(show_log):
    # Create 'local' directory
    create_dir(LOCAL_STORAGE_PATH, show_log)
    # Create 'scans' folder in 'local' directory
    create_dir(LOCAL_SCANS_PATH, show_log)
    # Create 'blacklist.txt' file in 'local' directory
    create_file(BLACKLIST_PATH, show_log)


def create_dir(dir_path, show):
    try:
        mkdir(dir_path)
        action = ' '.join(['create directory', dir_path])
        print_success(action, show)
    except FileExistsError as _:
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


def print_log(src, show):
    log_msg = ' '.join(['starting', src])
    if show:
        print(log_msg)


def get_scan_count():
    scans = listdir(LOCAL_SCANS_PATH)
    return len(scans)


def store_metadata(metadata):
    recent_scan = '_'.join(['scan', str(get_scan_count() + 1)])
    recent_scan_path = join(LOCAL_SCANS_PATH, recent_scan)
    with open(recent_scan_path, 'w') as file:
        for ip in metadata:
            entry = ' '.join([metadata[ip][value] for value in metadata[ip]] + [ip, '\n'])
            file.write(entry)
