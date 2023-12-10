import sys
import time
import traceback
import random


class CollectGender:

    def __init__(self, browser):
        self.browser = browser
        self.data = []

    def scrape_data(self, user_id, scan_list, section, elements_path, save_status):
        """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
        about_information = []
        page = []

        if save_status == 4:
            page.append(user_id)

        page += [user_id + s for s in section]

        for i, _ in enumerate(scan_list):
            try:
                self.browser.get(page[i])

                if (save_status == 0) or (save_status == 1) or (
                        save_status == 2):  # Only run this for friends, photos and videos

                    # the bar which contains all the sections
                    sections_bar = self.browser.find_element_by_xpath("//*[@class='_3cz'][1]/div[2]/div[1]")


                    if sections_bar.text.find(scan_list[i]) == -1:
                        continue

                if save_status != 3:
                    self.scroll()

                data = self.browser.find_elements_by_xpath(elements_path[i])
                self.delay = random.randrange(1, 5)
                time.sleep(self.delay)

                about_information.append(data[0].text.split("\n"))

                # save_to_file(file_names[i], data, save_status, i)
            except Exception:
                print("Exception (scrape_data)", str(i), "Status =", str(save_status), sys.exc_info()[0])
        return about_information

    def scrape_genger(self, user_id):
        try:
            scan_list = [None] * 2
            section = ["/about","/about?section=contact-info"]
            elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 2
            save_status = 3

            results = self.scrape_data(user_id, scan_list, section, elements_path, save_status)
            print(results)
            gender = None
            for i in range(len(results)):
                for j in range(len(results[i])):
                    if (results[i][j] == "Gender"):
                        gender = results[i][j + 1]
                        break
            print("About Section Done!",gender)
            return gender
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            return None

    def retrive_gender(self,profile_link):
        gender = self.scrape_genger(profile_link)
        return gender
