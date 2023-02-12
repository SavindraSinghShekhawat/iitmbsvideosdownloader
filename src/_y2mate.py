import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Y2mate:
    # downloads all files from y2mate
    def download_files(self, driver, video_links, yt_video_titles):
        titles = list(video_links.keys())
        time.sleep(self.SLEEP_TIME)
        i = 0
        for video_id in video_links.values():
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            time.sleep(self.SLEEP_TIME)
            i += 1

    # downloads a file and retries if failed
    def download_file(self, driver, i, video_id, titles, yt_video_titles):
        self.log(f"--> {titles[i]}...", 2)
        driver.get("https://www.y2mate.com/")
        self.wait_for_element_by_class(driver, "input-lg", 20)
        time.sleep(self.SLEEP_TIME)
        input_field = driver.find_element(By.CLASS_NAME, "input-lg")
        input_field.send_keys(f"https://www.youtube.com/watch?v={video_id}")
        self.log("Input Entered", 3)
        time.sleep(self.SLEEP_TIME)

        button = driver.find_element(By.ID, "btn-submit")
        button.click()
        self.log("Submit Button Clicked", 3)

        self.wait_for_element_by_class(driver, "btn-success", 20)
        time.sleep(self.SLEEP_TIME)
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
        time.sleep(self.SLEEP_TIME)
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
