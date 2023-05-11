# coding=utf-8

import os
import time

import requests

_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36'
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
    res = requests.get(url.strip(), headers=_headers)
    res.close()
    if res.status_code == 200:
        return parse_text(res.text)
    return []


def merge_tracker_list(all_tracker_lists: []) -> set:
    s = set(all_tracker_lists)
    s.remove('')
    return s


def write_to_file(merged_results: set, output_file_name="all.txt"):
    with open(file=output_file_name, mode="w", encoding="utf8") as f:
        for r in merged_results:
            f.write(r)
            f.write("\n")


def move_file(output_file_name="all.txt", backup_dir="daily_back/all_"):
    os.rename(output_file_name, backup_dir + time.strftime("%Y-%m-%d", time.localtime()) + ".txt")


if __name__ == '__main__':
    config_list = [{"config": "config.txt",
                    "file": "all.txt",
                    "backup_dir": "daily_back/all_"
                    }
        ,

                   {"config": "config_best.txt",
                    "file": "best_all.txt",
                    "backup_dir": "daily_back/best_all_"
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
            move_file(i['file'], i['backup_dir'])
            write_to_file(merged_result, i['file'])
