import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from iitmbsvideosdownloader.functions import wait_for_element_by_class, download_wait, log, newest, beautify_file_name, normalize


# downloads a file and retries if failed
def download_file(driver, DOWNLOAD_DIRECTORY, i, video_id, titles, yt_video_titles):
    log(f"--> {titles[i]}...")
    driver.get("https://www.y2mate.com/")
    wait_for_element_by_class(driver, "input-lg", 20)
    input_field = driver.find_element(By.CLASS_NAME, "input-lg")
    input_field.send_keys(f"https://www.youtube.com/watch?v={video_id}")
    log("Input Entered")

    button = driver.find_element(By.ID, "btn-submit")
    button.click()
    log("Submit Button Clicked")

    wait_for_element_by_class(driver, "btn-success", 20)

    downloadButtons = None
    failure_ = True
    while failure_:
        try:
            downloadButtons = driver.find_elements(By.CLASS_NAME, "btn-success")
            failure_ = False
        except NoSuchElementException:
            failure_ = True
    downloadButtons[1].click()
    log("Download Button Clicked")

    wait_for_element_by_class(driver, "btn-file", 20)

    downloadButton = None
    failure_ = True
    while failure_:
        try:
            downloadButton = driver.find_element(By.CLASS_NAME, "btn-file")
            failure_ = False
        except NoSuchElementException:
            failure_ = True

    downloadButton.click()
    log("Download Button from Popup Clicked, Downloading...")

    download_wait(DOWNLOAD_DIRECTORY)

    log("Download Assumed")

    if newest(DOWNLOAD_DIRECTORY) is None:
        log("Download failed, Retrying...")
        download_file(driver, DOWNLOAD_DIRECTORY, i, video_id, titles, yt_video_titles)
        return

    newest_file, extension = newest(DOWNLOAD_DIRECTORY)

    yt_title = yt_video_titles[i]

    if normalize(yt_title) not in normalize(newest_file):
        log("Download failed, Retrying...")
        download_file(driver, DOWNLOAD_DIRECTORY, i, video_id, titles, yt_video_titles)
        return

    log("Download Verified")
    os.rename(newest_file, os.path.join(DOWNLOAD_DIRECTORY, beautify_file_name(titles[i]) + extension))

    log("File Renamed")


# downloads all files from y2mate
def download_files(driver, video_links, DOWNLOAD_DIRECTORY, yt_video_titles):
    titles = list(video_links.keys())
    i = 0
    for video_id in video_links.values():
        download_file(driver, DOWNLOAD_DIRECTORY, i, video_id, titles, yt_video_titles)
        i += 1
