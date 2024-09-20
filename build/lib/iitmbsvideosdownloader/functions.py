import os
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from iitmbsvideosdownloader.variables import DEBUG


# waits for an element to appear by ID
def wait_for_element_by_id(driver, element_id, timeout):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
    except TimeoutException:
        return None


# waits for an element to appear by Class name
def wait_for_element_by_class(driver, element_class, timeout):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
    except TimeoutException:
        return None


# waits for an element to appear by xPath
def wait_for_element_by_xPath(driver, element_xPath, timeout):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_xPath)))
    except TimeoutException:
        return None


# waits for an element to appear by xPath
def wait_for_element_by_tag(driver, element_tag, timeout):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, element_tag)))
    except TimeoutException:
        return None


# checks if any ongoing downloads
def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait:
        time.sleep(5)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds


# logging if DEBUG == True
def log(s):
    if DEBUG:
        print(s)


# gets the newest .mp4 or .webm file in path
def newest(path):
    files = os.listdir(path)
    final_files = {}

    for f in files:
        if f.endswith(".mp4"):
            final_files[f] = ".mp4"
        elif f.endswith(".webm"):
            final_files[f] = ".webm"

    if len(list(final_files.keys())) == 0:
        return None

    paths = [os.path.join(path, basename) for basename in final_files.keys()]

    newest_file = max(paths, key=os.path.getctime)
    file_name = newest_file.split("\\")[-1]
    ext = final_files[file_name]
    return newest_file, ext


# beautifies name of file, for ex: puts L in starting if it's not there and makes something like L1.2 -
def beautify_file_name(string):
    filename = string
    if re.match("^L\d+.\d+ - ", filename) is None:
        if ':' not in filename:
            if filename.startswith("L"):
                spl = filename.split(" ")
                l = [i for i in spl if i != ""]
                if len(l) > 1:
                    filename = l[0] + " - " + ' '.join(l[1:])
            else:
                spl = filename.split(" ")
                l = [i for i in spl if i != ""]
                if len(l) > 1:
                    filename = "L" + l[0] + " - " + ' '.join(l[1:])
        else:
            filename = filename.replace(":", " -")
    return valid_file_name(filename)


# returns a valid filename by removing characters that are not allowed in filenames
def valid_file_name(filename):
    for char in filename:
        if char in ['\\', '/', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, "")
    return filename


# return only A-Z and a-z of a string, helps in making sure video with the YouTube title is same as filename of video
# downloaded from y2mate, which helps in renaming the right files in order
def normalize(filename):
    result = ""
    for char in filename:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            result += char
    return result
