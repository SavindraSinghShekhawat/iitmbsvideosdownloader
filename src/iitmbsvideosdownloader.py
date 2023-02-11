import os
import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from iitmbsvideosdownloader.SUBJECTS import _Subject


class SmartBot:
    MY_TERM = 7  # the folder will be renamed to "Term {MYTERM}"
    WEEK = 3  # current week, helps in getting the right week videos from portal and creating folders
    YEAR = 23  # current Year last 2 digits, helps in getting right url of iitm portal
    TERM = 1  # current term of the year (1 for Jan, 2 for May, 3 for Sep)

    # browser's location to run (prefer Brave)
    BROWSER_LOCATION = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    # if more than 1 profile in browser, enter its location and profile folder name
    # usually it's "Profile 1" for a second profile
    USER_DATA_DIRECTORY = "C:\\Users\\Shekh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"
    PROFILE = "Default"  # leave it to "Default" if only one profile

    # sleeps help in waiting for page to load, if your internet speed is good 2 is fine, try increasing if you face
    # errors
    SLEEP_TIME = 2

    # Directory of current term
    MAIN_DIRECTORY = f"D:\\Term {MY_TERM}"

    # subjects with their subject_code, helps in creating folders for each subjects in MAIN_DIRECTORY and subject code
    # allows to load iitm portal of the subject
    SELECTED_SUBJECTS = []

    DOWNLOAD_DIRECTORY = None

    DEBUG = True
    VERBOSE = 4

    # sets self.logging to True, if you want to find out where something went wrong

    def __init__(self, browser_path: str, download_path: str, user_data_path: str, profile_name: str, subjects: list,
                 year: int, term: int, week: int, sleep_time: int = 2, debug: bool = True, verbose: int = 2):

        self.DOWNLOAD_DIRECTORY = None
        self.check_argumnets(browser_path, download_path, user_data_path, profile_name, subjects, year, term, week,
                             sleep_time=2, debug=True, verbose=2)

        self.BROWSER_LOCATION = browser_path
        self.USER_DATA_DIRECTORY = user_data_path
        self.MAIN_DIRECTORY = download_path
        self.PROFILE = profile_name
        self.SELECTED_SUBJECTS = subjects
        self.YEAR = year
        self.TERM = term
        self.WEEK = week
        self.SLEEP_TIME = sleep_time
        VERBOSE = verbose
        DEBUG = debug

    def start(self):
        options = webdriver.ChromeOptions()
        options.binary_location = self.BROWSER_LOCATION
        # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        prefs = {
            # "download.default_directory": DOWNLOAD_DIRECTORY,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        }

        options.add_argument(f'profile-directory={self.PROFILE}')
        options.add_argument(f"user-data-dir={self.USER_DATA_DIRECTORY}")

        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        i = 1
        # loop for each subject, makes sure all subjects are downloaded in their respected folders.
        for subject in self.SELECTED_SUBJECTS:
            subject_name = subject.name
            subject_code = subject.code

            self.log("-----------------------------------------------------", 1)
            self.log(f"Subject {i} - {subject_name}", 1)

            self.DOWNLOAD_DIRECTORY = os.path.join(self.MAIN_DIRECTORY, subject_name, f"Week{self.WEEK}")
            URL = f"https://seek.onlinedegree.iitm.ac.in/courses/ns_{self.YEAR}t{self.TERM}_{subject_code}"
            self.log(f"URL - {URL}", 2)

            params = {'behavior': 'allow', 'downloadPath': self.DOWNLOAD_DIRECTORY}
            driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

            self.log(f"Download path changed to {self.DOWNLOAD_DIRECTORY}", 2)

            self.downloadSubjectVideos(driver, URL)

            self.log("Download done for this subject!", 1)

            i += 1

        driver.close()

    def downloadSubjectVideos(self, driver, URL):
        driver.get(URL)
        self.log(f"Getting Titles and links...", 1)
        titles_with_links, yt_video_titles = self.get_video_titles_and_links(driver)
        self.log(f"\nDownloading videos...", 1)
        self.download_files(driver, titles_with_links, yt_video_titles)

    def get_video_titles_and_links(self, driver):
        self.wait_for_element_by_class(driver, "units__items", 20)
        time.sleep(self.SLEEP_TIME * 2)
        side_elements = driver.find_elements(By.CLASS_NAME, "units__items")

        self.wait_for_element_by_class(driver, "units__items-title", 20)
        # time.sleep(SLEEP_TIME / 2)
        side_titles_elements = driver.find_elements(By.CLASS_NAME, "units__items-title")
        side_titles_text = [side_titles_elements[i].text for i in range(len(side_titles_elements))]

        self.log(f"Side titles - {side_titles_text}", 3)

        index_title = side_titles_text.index(f"Week {self.WEEK}")
        self.log(f"Selected side title - {side_titles_text[index_title]}", 3)

        side_elements[index_title].click()

        self.wait_for_element_by_xPath(driver, "//div[contains(@class, 'units__sublist')]/div", 20)
        # time.sleep(SLEEP_TIME / 2)
        sub_items_elements = side_elements[index_title].find_elements(By.XPATH,
                                                                      "div[contains(@class, 'units__sublist')]/div")

        titles = []
        for element in sub_items_elements:
            title = element.find_element(By.XPATH, "div/div[contains(@class, 'units__subitems-title')]/span")
            text = title.get_attribute("innerHTML")
            result = re.sub(r'<!(-)+>', '', text)
            titles.append(result)

        titles_with_links = {}
        yt_video_titles = []

        self.log(f"Sub side titles - {titles}", 3)

        # Getting video links
        for i in range(len(sub_items_elements)):
            element = sub_items_elements[i]
            # time.sleep(SLEEP_TIME / 2)
            self.wait_for_element_by_xPath(element, "div/div[contains(@class, 'units__subitems-title')]/div", 20)
            video_text = element.find_element(By.XPATH, "div/div[contains(@class, 'units__subitems-title')]/div")

            text = video_text.get_attribute("innerHTML")
            result = re.sub(r'<!(-)+>', '', text)
            if result == "Video":
                self.log(f"--> Grabbing sub side title ({titles[i]}) details...", 3)
                element.click()

                self.wait_for_element_by_xPath(driver, "//iframe[contains(@id, 'player')]", 20)
                # time.sleep(SLEEP_TIME / 2)
                driver.switch_to.frame("player")

                self.wait_for_element_by_class(driver, "ytp-cued-thumbnail-overlay-image", 20)
                videoID = self.get_videoID(driver)
                self.log(f"video ID - {videoID}", 4)
                titles_with_links[f"{titles[i]}"] = videoID

                self.wait_for_element_by_class(driver, "ytp-title-link", 20)
                a = driver.find_element(By.CLASS_NAME, "ytp-title-link")
                yt_video_title = a.get_attribute("innerHTML")
                self.log(f"Youtube title - {yt_video_title}", 4)
                yt_video_titles.append(yt_video_title)

                driver.switch_to.default_content()

        return titles_with_links, yt_video_titles

    # downloads all files from y2mate
    def download_files(self, driver, video_links, yt_video_titles):
        titles = list(video_links.keys())
        i = 0
        for video_id in video_links.values():
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            i += 1

    # downloads a file and retries if failed
    def download_file(self, driver, i, video_id, titles, yt_video_titles):
        self.log(f"--> {titles[i]}...", 2)
        driver.get("https://www.y2mate.com/")
        self.wait_for_element_by_class(driver, "input-lg", 20)
        input_field = driver.find_element(By.CLASS_NAME, "input-lg")
        input_field.send_keys(f"https://www.youtube.com/watch?v={video_id}")
        self.log("Input Entered", 3)

        button = driver.find_element(By.ID, "btn-submit")
        button.click()
        self.log("Submit Button Clicked", 3)

        self.wait_for_element_by_class(driver, "btn-success", 20)

        downloadButtons = None
        failure_ = True
        while failure_:
            try:
                downloadButtons = driver.find_elements(By.CLASS_NAME, "btn-success")
                failure_ = False
            except NoSuchElementException:
                failure_ = True
        downloadButtons[1].click()
        self.log("Download Button Clicked", 3)

        self.wait_for_element_by_class(driver, "btn-file", 20)

        downloadButton = None
        failure_ = True
        while failure_:
            try:
                downloadButton = driver.find_element(By.CLASS_NAME, "btn-file")
                failure_ = False
            except NoSuchElementException:
                failure_ = True

        downloadButton.click()
        self.log("Download Button from Popup Clicked, Downloading...", 3)

        self.download_wait(self.DOWNLOAD_DIRECTORY)

        self.log("Download Assumed", 2)

        if self.newest(self.DOWNLOAD_DIRECTORY) is None:
            self.log("Download failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        newest_file, extension = self.newest(self.DOWNLOAD_DIRECTORY)

        yt_title = yt_video_titles[i]

        if self.normalize(yt_title) not in self.normalize(newest_file):
            self.log("Download failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        self.log("Download Verified", 2)
        os.rename(newest_file, os.path.join(self.DOWNLOAD_DIRECTORY, self.beautify_file_name(titles[i]) + extension))

        self.log("File Renamed", 3)

    def check_argumnets(self, browser_path: str, download_path: str, user_data_path: str, profile_name: str,
                        subjects: list,
                        year: int, term: int, week: int, sleep_time: int = 2, debug: bool = True, verbose: int = 2):
        if not (os.path.isfile(browser_path)):
            raise Exception("browser_path is not valid.")
        if not (os.path.isdir(download_path)):
            raise Exception("download_path is not valid.")
        if not (os.path.isdir(user_data_path)):
            raise Exception("user_data_path is not valid.")
        if not (os.path.isdir(os.path.join(user_data_path, profile_name))):
            raise Exception("profile_name is not valid.")
        for sub in subjects:
            if type(sub) != _Subject:
                raise Exception("Subjects should be used from SUBJECTS, for ex: SUBJECTS.ENGLISH_I")
        if len(subjects) < 1 or len(subjects) > 4:
            raise Exception("subjects should be 4 or less.")
        if year < 20 or year > 29:
            raise Exception("year provided should be in two digits integer for ex: 23")
        if term not in [1, 2, 3]:
            raise Exception(
                "term should be an integer between 1 to 3, for ex: 1 for Jan Term, 2 for May Term, 3 for Sep Term")
        if week not in list(range(13)):
            raise Exception("week should be between 0 to 12")
        if sleep_time < 2:
            raise Exception("sleep_time should be 2 or more seconds")
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
    def beautify_file_name(self, string):
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
        return string.valid_file_name(filename)

    # returns a valid filename by removing characters that are not allowed in filenames
    def valid_file_name(self, filename):
        for char in filename:
            if char in ['\\', '/', '*', '?', '"', '<', '>', '|']:
                filename = filename.replace(char, "")
        return filename

    # return only A-Z and a-z of a string, helps in making sure video with the YouTube title is same as filename of video
    # downloaded from y2mate, which helps in renaming the right files in order
    def normalize(self, filename):
        result = ""
        for char in filename:
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                result += char
        return result
