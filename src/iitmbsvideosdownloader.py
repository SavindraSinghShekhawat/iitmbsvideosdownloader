import os

from selenium import webdriver

from iitmbsvideosdownloader._iitm import IITM
from iitmbsvideosdownloader._functions import Functions
from iitmbsvideosdownloader._downloader import Downloader

from iitmbsvideosdownloader.SITES import _Site
from iitmbsvideosdownloader import SITES


class SmartBot(IITM, Functions, Downloader):
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
    SLEEP_TIME = 0

    # Directory of current term
    MAIN_DIRECTORY = f"D:\\Term {MY_TERM}"

    # subjects with their subject_code, helps in creating folders for each subjects in MAIN_DIRECTORY and subject code
    # allows to load iitm portal of the subject
    SELECTED_SUBJECTS = []

    DOWNLOAD_DIRECTORY = None

    DEBUG = True
    VERBOSE = 4

    DOWNLOAD_SITE = SITES.Y2MATE

    # sets self.logging to True, if you want to find out where something went wrong

    def __init__(self, browser_path: str, download_path: str, user_data_path: str, profile_name: str, subjects: list,
                 year: int, term: int, week: int, download_site: _Site = SITES.Y2MATE, sleep_time: int = 0,
                 debug: bool = True, verbose: int = 2):
        self.check_argumnets(browser_path, download_path, user_data_path, profile_name, subjects, year, term, week,
                             download_site,
                             sleep_time=0, debug=True, verbose=2)

        self.BROWSER_LOCATION = browser_path
        self.USER_DATA_DIRECTORY = user_data_path
        self.MAIN_DIRECTORY = download_path
        self.PROFILE = profile_name
        self.SELECTED_SUBJECTS = subjects
        self.YEAR = year
        self.TERM = term
        self.WEEK = week
        self.DOWNLOAD_SITE = download_site
        self.SLEEP_TIME = sleep_time
        self.VERBOSE = verbose
        self.DEBUG = debug

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
