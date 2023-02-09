import re
import time

from selenium.webdriver.common.by import By

from iitmbsvideosdownloader._functions import wait_for_element_by_class, wait_for_element_by_xPath, log
from iitmbsvideosdownloader._variables import WEEK, SLEEP_TIME
from iitmbsvideosdownloader._y2mate import download_files


# gets video titles by clicking each of the video items from left side panel
def get_video_titles_and_links(driver):
    wait_for_element_by_class(driver, "units__items", 20)
    time.sleep(SLEEP_TIME * 2)
    side_elements = driver.find_elements(By.CLASS_NAME, "units__items")

    wait_for_element_by_class(driver, "units__items-title", 20)
    # time.sleep(SLEEP_TIME / 2)
    side_titles_elements = driver.find_elements(By.CLASS_NAME, "units__items-title")
    side_titles_text = [side_titles_elements[i].text for i in range(len(side_titles_elements))]

    log(f"Side titles - {side_titles_text}", 3)

    index_title = side_titles_text.index(f"Week {WEEK}")
    log(f"Selected side title - {side_titles_text[index_title]}", 3)

    side_elements[index_title].click()

    wait_for_element_by_xPath(driver, "//div[contains(@class, 'units__sublist')]/div", 20)
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

    log(f"Sub side titles - {titles}", 3)

    # Getting video links
    for i in range(len(sub_items_elements)):
        element = sub_items_elements[i]
        # time.sleep(SLEEP_TIME / 2)
        wait_for_element_by_xPath(element, "div/div[contains(@class, 'units__subitems-title')]/div", 20)
        video_text = element.find_element(By.XPATH, "div/div[contains(@class, 'units__subitems-title')]/div")

        text = video_text.get_attribute("innerHTML")
        result = re.sub(r'<!(-)+>', '', text)
        if result == "Video":
            log(f"--> Grabbing sub side title ({titles[i]}) details...", 3)
            element.click()

            wait_for_element_by_xPath(driver, "//iframe[contains(@id, 'player')]", 20)
            # time.sleep(SLEEP_TIME / 2)
            driver.switch_to.frame("player")

            wait_for_element_by_class(driver, "ytp-cued-thumbnail-overlay-image", 20)
            videoID = get_videoID(driver)
            log(f"video ID - {videoID}", 4)
            titles_with_links[f"{titles[i]}"] = videoID

            wait_for_element_by_class(driver, "ytp-title-link", 20)
            a = driver.find_element(By.CLASS_NAME, "ytp-title-link")
            yt_video_title = a.get_attribute("innerHTML")
            log(f"Youtube title - {yt_video_title}", 4)
            yt_video_titles.append(yt_video_title)

            driver.switch_to.default_content()

    return titles_with_links, yt_video_titles


def get_videoID(driver):
    thumbnail = driver.find_element(By.CLASS_NAME, "ytp-cued-thumbnail-overlay-image")
    video_url = thumbnail.get_attribute("style")
    try:
        videoID = video_url.split("/")[4]
        return videoID
    except IndexError:
        return get_videoID(driver)


# starts and closes browser for subject given
def downloadSubjectVideos(driver, URL, DOWNLOAD_DIRECTORY):
    driver.get(URL)
    log(f"Getting Titles and links...", 1)
    titles_with_links, yt_video_titles = get_video_titles_and_links(driver)
    log(f"\nDownloading videos...", 1)
    download_files(driver, titles_with_links, DOWNLOAD_DIRECTORY, yt_video_titles)
