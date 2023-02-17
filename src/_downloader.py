import os
import time

from selenium.webdriver.common.by import By

from iitmbsvideosdownloader import SITES


class Downloader:
    # downloads all files from y2mate
    def download_files(self, driver, video_links, yt_video_titles):

        print(f"download_site is {self.DOWNLOAD_SITE.name}")

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

        if self.check_file_exists(self.beautify_file_name(titles[i]) + ".mp4") or self.check_file_exists(
                self.beautify_file_name(titles[i]) + ".webm"):
            self.log(self.beautify_file_name(titles[i]) + ".mp4")
            self.log("Already downloaded, skipping", 2)
            return

        # driver.get("https://www.y2mate.com/")

        driver.get(self.DOWNLOAD_SITE.url)

        if self.DOWNLOAD_SITE == SITES.Y2MATE:
            self.y2mate(driver, i, video_id, titles, yt_video_titles)
        elif self.DOWNLOAD_SITE == SITES.Y2META:
            self.y2meta(driver, i, video_id, titles, yt_video_titles)
        else:
            raise Exception("couldn't connect to download site.")

    def y2mate(self, driver, i, video_id, titles, yt_video_titles):
        input_lg_test = self.wait_for_element_by_class(driver, "input-lg", 20)

        if input_lg_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        time.sleep(self.SLEEP_TIME)
        input_field = driver.find_element(By.CLASS_NAME, "input-lg")
        input_field.send_keys(f"https://www.youtube.com/watch?v={video_id}")
        self.log("Input Entered", 3)
        time.sleep(self.SLEEP_TIME)

        button = driver.find_element(By.ID, "btn-submit")
        button.click()
        self.log("Submit Button Clicked", 3)

        buttons_test = self.wait_for_element_by_class(driver, "btn-success", 20)

        if buttons_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        time.sleep(self.SLEEP_TIME)
        downloadButtons = driver.find_elements(By.CLASS_NAME, "btn-success")

        if len(downloadButtons) <= 2:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        downloadButtons[1].click()
        self.log("Download Button Clicked", 3)

        btn_file_test = self.wait_for_element_by_class(driver, "btn-file", 20)

        if btn_file_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        downloadButton = driver.find_element(By.CLASS_NAME, "btn-file")

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
            # print(f"yt_title - {self.normalize(yt_title)}")
            # print(f"newest_file - {self.normalize(newest_file)}")
            self.log("Download failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        self.log("Download Verified", 2)
        os.rename(newest_file, os.path.join(self.DOWNLOAD_DIRECTORY, self.beautify_file_name(titles[i]) + extension))

        self.log("File Renamed", 3)

    def y2meta(self, driver, i, video_id, titles, yt_video_titles):
        input_lg_test = self.wait_for_element_by_class(driver, "input-lg", 20)

        if input_lg_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        time.sleep(self.SLEEP_TIME)
        input_field = driver.find_element(By.CLASS_NAME, "input-lg")
        input_field.send_keys(f"https://www.youtube.com/watch?v={video_id}")
        self.log("Input Entered", 3)
        time.sleep(self.SLEEP_TIME)

        button = driver.find_element(By.ID, "btn-submit")
        button.click()
        self.log("Submit Button Clicked", 3)

        buttons_test = self.wait_for_element_by_class(driver, "btn-success", 20)

        if buttons_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        time.sleep(self.SLEEP_TIME)
        downloadButtons = driver.find_elements(By.CLASS_NAME, "btn-success")

        if len(downloadButtons) < 2:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        downloadButtons[0].click()
        self.log("Download Button Clicked", 3)

        btn_file_test = self.wait_for_element_by_class(driver, "btn-download-link", 20)

        if btn_file_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            self.download_file(driver, i, video_id, titles, yt_video_titles)
            return

        downloadButton = driver.find_element(By.CLASS_NAME, "btn-download-link")

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