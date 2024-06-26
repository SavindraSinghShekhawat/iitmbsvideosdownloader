import os

from selenium import webdriver

from iitmbsvideosdownloader._iitm import IITM
from iitmbsvideosdownloader._functions import Functions
from iitmbsvideosdownloader._downloader import Downloader

from iitmbsvideosdownloader.SITES import _Site
from iitmbsvideosdownloader import SITES
import chromedriver_autoinstaller_fix
import requests


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

    DOWNLOAD_SITE = SITES.AUTO

    QUALITY = 5

    # sets self.logging to True, if you want to find out where something went wrong

    def __init__(self, executable_path: str, profile_path: str, download_path: str, subjects: list,
                 year: int, term: int, week: int, download_site: _Site = SITES.AUTO, sleep_time: int = 0,
                 debug: bool = True, verbose: int = 2, quality: int = 5):
        self.check_arguments(executable_path, profile_path, download_path, subjects, year, term, week,
                             download_site, sleep_time=0, debug=True, verbose=2, quality=quality)

        self.BROWSER_LOCATION = executable_path
        self.USER_DATA_DIRECTORY = os.path.dirname(os.path.normpath(profile_path))
        self.PROFILE = os.path.basename(os.path.normpath(profile_path))
        self.MAIN_DIRECTORY = download_path
        self.SELECTED_SUBJECTS = subjects
        self.YEAR = str(year)[2:]
        self.TERM = term
        self.WEEK = week
        self.DOWNLOAD_SITE = download_site
        self.SLEEP_TIME = sleep_time
        self.VERBOSE = verbose
        self.DEBUG = debug
        self.QUALITY = quality

        def get_working_downloader_site(download_site, timeout=0.2):
            if timeout >= 30:
                if download_site == SITES.AUTO:
                    raise Exception(
                        "Couldn't find any working site to download videos on your current internet connection.")
                else:
                    raise Exception(
                        f'Site {download_site.name} is not working on your current internet connection. Try Using default Site option as SITES.AUTO.')

            if download_site == SITES.AUTO:
                sites = [SITES.Y2MATE, SITES.Y2META]
                for site in sites:
                    try:
                        #print(site.name)
                        response = requests.head(site.url, timeout=timeout).status_code
                        if str(response).strip().isdigit():
                            download_site = site
                    except Exception as e:
                        pass
                        #print("Failed")

                if download_site == SITES.AUTO:
                    return get_working_downloader_site(download_site, timeout=timeout * 5)
                else:
                    return download_site
            elif download_site == SITES.Y2MATE:
                try:
                    response = requests.head(SITES.Y2MATE.url, timeout=timeout).status_code
                    if str(response).strip().isdigit():
                        return download_site
                except Exception as e:
                    return get_working_downloader_site(download_site, timeout=timeout * 5)

            elif download_site == SITES.Y2META:
                try:
                    response = requests.head(SITES.Y2META.url, timeout=timeout).status_code
                    if str(response).strip().isdigit():
                        return download_site
                except Exception as e:
                    return get_working_downloader_site(download_site, timeout=timeout * 5)

        final_site = get_working_downloader_site(download_site)
        self.DOWNLOAD_SITE = final_site
        self.log(f"Download Site is finalised to {final_site.name}.", 2)
        chromedriver_autoinstaller_fix.install()

    def start(self):
        options = webdriver.ChromeOptions()
        options.binary_location = self.BROWSER_LOCATION
        # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        prefs = {
            # "download.default_directory": DOWNLOAD_DIRECTORY,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": False
        }

        options.add_argument(f'profile-directory={self.PROFILE}')
        options.add_argument(f"user-data-dir={self.USER_DATA_DIRECTORY}")

        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)

        # service = ChromeService(executable_path=self.BROWSER_LOCATION)
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
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

            success = self.downloadSubjectVideos(driver, URL)

            if success:
                self.log("Download done for this subject!", 1)

            i += 1

        driver.close()
