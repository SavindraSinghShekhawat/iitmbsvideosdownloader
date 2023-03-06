import os
import re
import time

from iitmbsvideosdownloader.SUBJECTS import _Subject
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from iitmbsvideosdownloader.SITES import _Site
from iitmbsvideosdownloader import SITES


class Functions:

    def check_argumnets(self, executable_path: str, profile_path: str, download_path: str, subjects: list,
                 year: int, term: int, week: int, download_site: _Site = SITES.Y2MATE, sleep_time: int = 0,
                 debug: bool = True, verbose: int = 2):
        if not (os.path.isfile(executable_path)):
            raise Exception("executable_path is not valid.")
        if not (os.path.isdir(profile_path)):
            raise Exception("profile_path is not valid.")
        if not (os.path.isdir(os.path.dirname(os.path.normpath(profile_path)))):
            raise Exception("profile_path is not valid.")
        if not (os.path.isdir(download_path)):
            raise Exception("download_path is not valid.")
        for sub in subjects:
            if type(sub) != _Subject:
                raise Exception("Subjects should be used from SUBJECTS, for ex: SUBJECTS.ENGLISH_I")
        if len(subjects) < 1 or len(subjects) > 4:
            raise Exception("subjects should be 4 or less.")
        if year < 2020 or year > 2029:
            raise Exception("year provided should be in between 2020 to 2029")
        if term not in [1, 2, 3]:
            raise Exception(
                "term should be an integer between 1 to 3, for ex: 1 for Jan Term, 2 for May Term, 3 for Sep Term")
        if week not in list(range(13)):
            raise Exception("week should be between 0 to 12")
        if type(download_site) != _Site:
            raise Exception("Site should be used from SITE, for ex: SITE.Y2MATE")
        if sleep_time < 0:
            raise Exception("sleep_time should be 0 or more seconds")
        if verbose < 0:
            raise Exception("verbose should be 0 or more")

    def get_videoID(self, driver):
        thumbnail = driver.find_element(By.CLASS_NAME, "ytp-cued-thumbnail-overlay-image")
        video_url = thumbnail.get_attribute("style")
        try:
            videoID = video_url.split("/")[4]
            return videoID
        except IndexError:
            return self.get_videoID(driver)

    # waits for an element to appear by ID
    def wait_for_element_by_id(self, driver, element_id, timeout):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
        except TimeoutException:
            return None

    # waits for an element to appear by Class name
    def wait_for_element_by_class(self, driver, element_class, timeout):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
        except TimeoutException:
            return None

    # waits for an element to appear by xPath
    def wait_for_element_by_xPath(self, driver, element_xPath, timeout):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_xPath)))
        except TimeoutException:
            return None

    # waits for an element to appear by xPath
    def wait_for_element_by_tag(self, driver, element_tag, timeout):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, element_tag)))
        except TimeoutException:
            return None

    # checks if any ongoing downloads
    def download_wait(self, path_to_downloads):
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
    def log(self, s, verbose=0):
        if self.DEBUG:
            if self.VERBOSE >= verbose:
                print(s)

    def check_file_exists(self, filename):
        return os.path.isfile(os.path.join(self.DOWNLOAD_DIRECTORY, filename))

    # gets the newest .mp4 or .webm file in path
    def newest(self, path):
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
    def beautify_file_name(self, filename):
        if "&amp;" in filename:
            filename = filename.replace("&amp;", "&")
        filename = filename.replace("  ", " ")
        filename = filename.replace(" : ", " - ")
        filename = filename.replace(": ", " - ")
        filename = filename.replace(" :", " - ")
        filename = filename.replace(":", " - ")

        if re.match("^L\d+.\d+\s+-\s+\w", filename) is not None:
            pass
        elif re.match("^\d+.\d+\s+-\s+\w", filename) is not None:
            filename = "L" + filename
        elif re.match("^L\d+.\d+\s+\w", filename) is not None:
            result = re.split("L\d+.\d+\s+", filename)[1]
            lecture = re.split(result, filename)[0]
            filename = lecture + "- " + result
        elif re.match("\d+.\d+\s+\w", filename) is not None:
            filename = "L" + filename
            result = re.split("L\d+.\d+\s+", filename)[1]
            lecture = re.split(result, filename)[0]
            filename = lecture + "- " + result
        return self.valid_file_name(filename)

    # returns a valid filename by removing characters that are not allowed in filenames
    def valid_file_name(self, filename):
        for char in filename:
            if char in ['\\', '/', '*', '?', '"', '<', '>', '|', '\n', '\t', "'", '\r', '\b']:
                filename = filename.replace(char, "")
        return filename

    # return only A-Z and a-z of a string, helps in making sure video with the YouTube title is same as filename of
    # video downloaded from y2mate, which helps in renaming the right files in order
    def normalize(self, filename):
        result = ""
        if "&amp;" in filename:
            filename = filename.replace("&amp;", "&")

        for char in filename:
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                result += char
        return result
