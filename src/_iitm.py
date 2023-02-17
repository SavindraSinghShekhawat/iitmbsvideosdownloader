import re
import time

from selenium.webdriver.common.by import By


class IITM:
    def downloadSubjectVideos(self, driver, URL):
        driver.get(URL)
        self.log(f"Getting Titles and links...", 1)
        titles_with_links, yt_video_titles = self.get_video_titles_and_links(driver)
        self.log(f"\nDownloading videos...", 1)
        self.download_files(driver, titles_with_links, yt_video_titles)

    def get_video_titles_and_links(self, driver):
        units_items_test = self.wait_for_element_by_class(driver, "units__items", 20)

        if units_items_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            return self.get_video_titles_and_links(driver)

        time.sleep(self.SLEEP_TIME + 4)
        side_elements = driver.find_elements(By.CLASS_NAME, "units__items")

        units_items_title_test = self.wait_for_element_by_class(driver, "units__items-title", 20)

        if units_items_title_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            return self.get_video_titles_and_links(driver)

        time.sleep(self.SLEEP_TIME)
        side_titles_elements = driver.find_elements(By.CLASS_NAME, "units__items-title")
        side_titles_text = [side_titles_elements[i].text for i in range(len(side_titles_elements))]

        self.log(f"Side titles - {side_titles_text}", 3)

        index_title = side_titles_text.index(f"Week {self.WEEK}")
        self.log(f"Selected side title - {side_titles_text[index_title]}", 3)

        side_elements[index_title].click()

        units_sublist_test = self.wait_for_element_by_xPath(driver, "//div[contains(@class, 'units__sublist')]/div", 20)

        if units_sublist_test is None:
            self.log("Finding an element failed, Retrying...", 2)
            return self.get_video_titles_and_links(driver)

        time.sleep(self.SLEEP_TIME)
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
            # time.sleep(self.SLEEP_TIME)
            units_subitem_title_test = self.wait_for_element_by_xPath(element, "div/div[contains(@class, 'units__subitems-title')]/div", 20)

            if units_subitem_title_test is None:
                self.log("Finding an element failed, Retrying...", 2)
                return self.get_video_titles_and_links(driver)

            video_text = element.find_element(By.XPATH, "div/div[contains(@class, 'units__subitems-title')]/div")

            text = video_text.get_attribute("innerHTML")
            result = re.sub(r'<!(-)+>', '', text)
            if result == "Video":
                self.log(f"--> Grabbing sub side title ({titles[i]}) details...", 3)
                element.click()

                player_test = self.wait_for_element_by_xPath(driver, "//iframe[contains(@id, 'player')]", 20)

                if player_test is None:
                    self.log("Finding an element failed, Retrying...", 2)
                    return self.get_video_titles_and_links(driver)

                time.sleep(self.SLEEP_TIME)
                driver.switch_to.frame("player")

                thumbnail_image_test = self.wait_for_element_by_class(driver, "ytp-cued-thumbnail-overlay-image", 20)

                if thumbnail_image_test is None:
                    self.log("Finding an element failed, Retrying...", 2)
                    return self.get_video_titles_and_links(driver)

                videoID = self.get_videoID(driver)
                self.log(f"video ID - {videoID}", 4)
                titles_with_links[f"{titles[i]}"] = videoID

                ytp_title_link_test = self.wait_for_element_by_class(driver, "ytp-title-link", 20)

                if ytp_title_link_test is None:
                    self.log("Finding an element failed, Retrying...", 2)
                    return self.get_video_titles_and_links(driver)

                a = driver.find_element(By.CLASS_NAME, "ytp-title-link")
                yt_video_title = a.get_attribute("innerHTML")
                self.log(f"Youtube title - {yt_video_title}", 4)
                yt_video_titles.append(yt_video_title)

                driver.switch_to.default_content()

        return titles_with_links, yt_video_titles
