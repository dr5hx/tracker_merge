# coding=utf-8

import os
import time
import re
import requests

_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.66 Safari/537.36'
}


def read_conf(confile_file="config.txt") -> []:
    t = None
    try:
        t = open(confile_file, mode="r", encoding="utf8")
        return t.readlines()
    finally:
        if t is not None:
            t.close()


def parse_text(text: str) -> []:
    return text.split("\n\n")


def get_trackers(url: str) -> []:
    s = requests.session()
    s.keep_alive = False
    res = s.get(url.strip(), headers=_headers)

    res.close()
    if res.status_code == 200:
        return parse_text(res.text)
    return []


def merge_tracker_list(all_tracker_lists: []) -> set:
    s = set(all_tracker_lists)
    if '' in s:
        s.remove('')
    return s


def write_to_file(merged_results: set, output_file_name="all.txt"):
    with open(file=output_file_name, mode="w", encoding="utf8") as f:
        for r in merged_results:
            f.write(r)
            f.write("\n")


def move_file(output_file_name="all.txt", backup_dir="daily_back/all_"):
    # backup_dir is passed as "daily_back/all_" (directory + prefix)
    base_dir = os.path.dirname(backup_dir)
    file_prefix = os.path.basename(backup_dir)
    
    current_time = time.localtime()
    year = time.strftime("%Y", current_time)
    month = time.strftime("%m", current_time)
    
    # Create directory structure: daily_back/YYYY/MM
    target_dir = os.path.join(base_dir, year, month)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    dest_file = os.path.join(target_dir, file_prefix + time.strftime("%Y-%m-%d", current_time) + ".txt")
    
    if not os.path.exists(output_file_name):
        return
    if os.path.exists(dest_file):
        os.remove(dest_file)
    os.rename(output_file_name, dest_file)


def process_history_data(backup_root="daily_back"):
    """
    Process existing files in the backup directory and move them to Year/Month subfolders.
    Matches files with pattern: prefix_YYYY-MM-DD.txt
    """
    if not os.path.exists(backup_root):
        print("Backup directory {} does not exist.".format(backup_root))
        return

    # Pattern to match files like all_2023-05-11.txt
    pattern = re.compile(r"^(.*_)(\d{4})-(\d{2})-(\d{2})\.txt$")
    
    files = os.listdir(backup_root)
    count = 0
    
    for filename in files:
        file_path = os.path.join(backup_root, filename)
        if os.path.isdir(file_path):
            continue
            
        match = pattern.match(filename)
        if match:
            prefix, year, month, day = match.groups()
            
            # Create target directory
            target_dir = os.path.join(backup_root, year, month)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            dest_path = os.path.join(target_dir, filename)
            
            try:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                os.rename(file_path, dest_path)
                count += 1
            except Exception as e:
                print("Error moving {}: {}".format(filename, e))
                
    print("Processed {} historical files.".format(count))


if __name__ == '__main__':
    # Process historical data first
    process_history_data()

    config_list = [{"config": "config.txt",
                    "file": "all.txt",
                    "daily_back": "daily_back/all_"
                    }
        ,

                   {"config": "config_best.txt",
                    "file": "best_all.txt",
                    "daily_back": "daily_back/best_all_"
                    }
                   ]
    for i in config_list:
        conf_list = read_conf(i['config'])
        all_tracker_list = []
        for conf in conf_list:
            tracker_list = get_trackers(conf)
            all_tracker_list.extend(tracker_list)
            print("current size is {}".format(len(all_tracker_list)))
            merged_result = merge_tracker_list(all_tracker_list)
            print("merged size is {}".format(len(merged_result)))
            move_file(i['file'], i['daily_back'])
            write_to_file(merged_result, i['file'])
