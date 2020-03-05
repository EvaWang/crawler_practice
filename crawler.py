# import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import os


def read_links_from_json(folder_path):
    files = os.listdir(folder_path)
    if len(files) <= 0:
        raise Exception('Empty queue.') 
        
    return read_from_json(os.path.join(folder_path, files[0])), files[0]

def mission_done(file_folder, filename):
    done_folder = "./done"
    create_folder(done_folder)

    ori_path = os.path.join(file_folder, filename)
    new_path = os.path.join(done_folder, filename)
    os.rename(ori_path, new_path)

def create_folder(path):
    is_exist = check_path_exist(path)
    if is_exist == False:
        os.mkdir(path)

def check_path_exist(path):
    return os.path.exists(path)

def save2json(filename, target_data):
    with open('%s.json'%filename, 'w') as outfile:
        json.dump(target_data, outfile, ensure_ascii=False)
    pass

def get_web_content(url, sleep=True):
    fake_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    # GET request from url and parse via BeautifulSoup
    r = requests.get(url, fake_headers)
    # 擷取request回傳的文字部分
    web_content = r.text

    # 記得sleep 不然ip會被鎖ＲＲＲ
    if sleep:
        print("take a rest.")
        time.sleep(5)

    return web_content

def get_from_api(url):
    r = requests.get(url)

    print("take a rest.")
    time.sleep(5)
    return r.json()

def read_from_json(filepath):
    with open(filepath) as f:
        obj = json.load(f)
    return obj

def sleep_test():
    for i in range(0, 10):
        print(datetime.datetime.now())
        time.sleep(5)

