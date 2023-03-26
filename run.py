# coding=utf-8

import os
import time

import requests

_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36'
}


def read_conf() -> []:
    t = None
    try:
        t = open("config.txt", mode="r", encoding="utf8")
        return t.readlines()
    finally:
        if t is not None:
            t.close()


def parse_text(text: str) -> []:
    return text.split("\n\n")


def get_trackers(url: str) -> []:
    res = requests.get(url.strip(), headers=_headers)
    if res.status_code == 200:
        return parse_text(res.text)
    return []


def merge_tracker_list(all_tracker_list: []) -> set:
    s = set(all_tracker_list)
    s.remove('')
    return s


def write_to_file(merged_result: set):
    with open(file="all.txt", mode="w", encoding="utf8") as f:
        for r in merged_result:
            f.write(r)
            f.write("\n")


def move_file():
    os.rename("all.txt", "daily_back/all_" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt")


if __name__ == '__main__':
    conf_list = read_conf()
    all_tracker_list = []
    for conf in conf_list:
        tracker_list = get_trackers(conf)
        all_tracker_list.extend(tracker_list)
    print("current size is {}".format(len(all_tracker_list)))
    merged_result = merge_tracker_list(all_tracker_list)
    print("merged size is {}".format(len(merged_result)))
    move_file()
    write_to_file(merged_result)
