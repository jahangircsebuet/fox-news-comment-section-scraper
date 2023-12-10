
class Page(object):

    def __init__(self,browser):
        self.browser = browser
        pass

    def collect_page(self, page):
        # navigate to page
        self.browser.get(
            'https://www.facebook.com/' + page + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            links = self.browser.find_elements_by_link_text("See More")
            for link in links:
                try:
                    link.click()
                except:
                    pass
            posts = self.browser.find_elements_by_class_name(
                "userContentWrapper")
            poster_names = self.browser.find_elements_by_xpath(
                "//a[@data-hovercard-referer]")

            for count, post in enumerate(posts):
                # Creating first CSV row entry with the poster name (eg. "Donald Trump")
                analysis = [poster_names[count].text]

                # Creating a time entry.
                time_element = post.find_element_by_css_selector("abbr")
                utime = time_element.get_attribute("data-utime")
                analysis.append(utime)

                # Creating post text entry
                text = post.find_element_by_class_name("userContent").text
                status = self.strip(text)
                analysis.append(status)

                # Write row to csv
                writer.writerow(analysis)