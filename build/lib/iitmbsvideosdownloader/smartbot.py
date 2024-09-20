from iitmbsvideosdownloader import SUBJECTS
from selenium import webdriver
import os

from iitmbsvideosdownloader._functions import log, check_argumnets
from iitmbsvideosdownloader._iitm import downloadSubjectVideos
from iitmbsvideosdownloader._variables import TERM, WEEK, MAIN_DIRECTORY, BROWSER_LOCATION, USER_DATA_DIRECTORY, PROFILE, \
    SELECTED_SUBJECTS, YEAR, SLEEP_TIME, VERBOSE, DEBUG


def start(browser_path: str, download_path: str, user_data_path: str, profile_name: str, subjects: list, year: int, term: int, week: int, sleep_time: int = 2, debug : bool = True, verbose: int = 2):
    check_argumnets(browser_path, download_path, user_data_path, profile_name, subjects, year, term, week, sleep_time = 2, debug = True, verbose = 2)

    BROWSER_LOCATION = browser_path
    USER_DATA_DIRECTORY = user_data_path
    MAIN_DIRECTORY = download_path
    PROFILE = profile_name
    SELECTED_SUBJECTS = subjects
    YEAR = year
    TERM = term
    WEEK = week
    SLEEP_TIME = sleep_time
    VERBOSE = verbose
    DEBUG = debug

    options = webdriver.ChromeOptions()
    options.binary_location = BROWSER_LOCATION
    # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    prefs = {
        # "download.default_directory": DOWNLOAD_DIRECTORY,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }

    options.add_argument(f'profile-directory={PROFILE}')
    options.add_argument(f"user-data-dir={USER_DATA_DIRECTORY}")

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    i = 1
    # loop for each subject, makes sure all subjects are downloaded in their respected folders.
    for subject in SELECTED_SUBJECTS:
        subject_name = subject.name
        subject_code = subject.code

        log("-----------------------------------------------------", 1)
        log(f"Subject {i} - {subject_name}", 1)

        DOWNLOAD_DIRECTORY = os.path.join(MAIN_DIRECTORY, subject_name, f"Week{WEEK}")
        URL = f"https://seek.onlinedegree.iitm.ac.in/courses/ns_{YEAR}t{TERM}_{subject_code}"
        log(f"URL - {URL}", 2)

        params = {'behavior': 'allow', 'downloadPath': DOWNLOAD_DIRECTORY}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

        log(f"Download path changed to {DOWNLOAD_DIRECTORY}", 2)

        downloadSubjectVideos(driver, URL, DOWNLOAD_DIRECTORY)

        log("Download done for this subject!", 1)

        i += 1

    driver.close()

'''
start(
    browser_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    download_path= "D:\\Term 7",
    user_data_path="C:\\Users\\Shekh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data",
    profile_name="Default",
    subjects=[
        SUBJECTS.AI_SEARCH_METHODS_FOR_PROBLEM_SOLVING,
        SUBJECTS.DEEP_LEARNING,
        SUBJECTS.SOFTWARE_ENGINEERING,
        SUBJECTS.STRATEGIES_FOR_PROFESSIONAL_GROWTH
    ],
    year=23,
    term=1,
    week=4,
)
'''