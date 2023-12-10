import time
import random
from browser import Browser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
from bs4 import BeautifulSoup


class FoxNewsChatgpt(object):
    def __init__(self, browser, depth):
        self.browser = browser
        self.depth = int(depth)

    def extract_message_info(self, message_div):
        # Extract user name, message, and timestamp from a message div
        user_name = message_div.find('span', class_='src-components-Username-index__wrapper').text
        timestamp = message_div.find('time', class_='Typography__text--11-4-12').text
        message = message_div.find('div', class_='richie-entities__entity__7d9542036c55fd69').p.text
        return {'user_name': user_name, 'timestamp': timestamp, 'message': message}

    def parse_tree(self, element):
        tree = {}
        ul_elements = element.find_elements(By.TAG_NAME, 'ul')
        for ul_element in ul_elements:
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
            tree[ul_element] = [self.parse_tree(li_element) for li_element in li_elements]
        return tree

    def check_element_exists(self, url):
        self.browser.get(url)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randrange(1, 5))

        # self.click_show_more_buttons()

        # Set a timeout for the implicit wait (if needed)
        self.browser.implicitly_wait(10)  # You can adjust the timeout as needed
        messages_wrapper_div = WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-spotim-module="conversation"]'))
        )
        print("messages_wrapper_div: ", messages_wrapper_div)

        inner_conversation = self.browser.execute_script(
            """return document.querySelector('[data-spotim-module="conversation"]').querySelector('div').shadowRoot.querySelector('[data-spot-im-module-default-area="conversation"]')"""
        )

        print("inner_conversation")
        print(inner_conversation)

        ul = inner_conversation.find_elements(By.XPATH, '//ul[@class="spcv_messages-list"]')
        # print("ul")
        # print(ul)
        ul = ul[0]

        first_level_li_elements = ul.find_elements_by_css_selector('li:not(li li)')
        print("first_level_li_elements.len: ", len(first_level_li_elements))

        i = 0
        for li in first_level_li_elements:

            article = li.find_element_by_tag_name("article")
            print(article)
            first_div = article.find_element_by_xpath(".//div")
            print("first_div html")
            print(first_div.get_attribute("outerHTML"))
            # print("first_div: ", first_div.text)
            outer_html = article.get_attribute("outerHTML")
            # print("outer_html: ", outer_html)
            # print("i: ", i)
            # if i < 2:
            #     print("soup i: ", i)
            #     # Parse the HTML content with BeautifulSoup
            #     soup = BeautifulSoup(outer_html, 'html.parser')
            #
            #     # Find the root message div
            #     root_message_div = soup.find('div', class_='spcv_rootComment')
            #
            #     # Extract information from the root message
            #     root_info = self.extract_message_info(root_message_div)
            #
            #     # Build the tree structure starting from the root
            #     comment_tree = self.build_tree(root_message_div)
            #
            #     # Print the extracted information (you can modify this part based on your needs)
            #     print("Root Message:", root_info)
            #     print("Comment Tree:", comment_tree)
            #
            #     i = i + 1

            # tree_structure = self.parse_tree(article)
            # print("tree_structure")
            # print(tree_structure)
            # print("Display tree structure")
            # self.display_tree(tree_structure)

            # p_tags = article.find_elements_by_tag_name("p")
            # print("p_tags.len: ", len(p_tags))
            # text_container = li.find_elements(By.XPATH, '//div[@data-spot-im-class="message-text"]')
            # p_elements = text_container[0].find_elements_by_tag_name("p")
            # for p in p_elements:
            #     print("p.text: ", p.text)

    def build_tree(self, node):
        # Recursively build the tree structure
        replies = []
        reply_divs = node.find('ul', class_='spcv_children-list').find_all('li')
        for reply_div in reply_divs:
            reply_info = self.extract_message_info(reply_div)
            reply_info['replies'] = self.build_tree(reply_div)
            replies.append(reply_info)
        return replies

    def click_show_more_buttons(self):
        print("click_show_more_buttons called")
        try:
            show_more_buttons = self.browser.find_elements(By.CLASS_NAME, 'spcv_show-more-repliesText')
            for button in show_more_buttons:
                button.click()
                # Wait for the next set of replies to load
                WebDriverWait(self.browser, 10).until(EC.staleness_of(button))
                self.click_show_more_buttons()  # Recursively click on "Show more" buttons

            # # Click on "Show n replies" buttons
            # show_n_replies_buttons = self.browser.find_elements(By.CLASS_NAME, 'spcv_showMoreRepliesText')
            # for button in show_n_replies_buttons:
            #     button.click()
            #     # Wait for the next set of replies to load
            #     WebDriverWait(self.browser, 10).until(EC.staleness_of(button))
            #     self.click_show_more_buttons()  # Recursively click on "Show more" buttons
            #
            # # Click on "n replies" buttons
            # n_replies_buttons = self.browser.find_elements(By.CLASS_NAME, 'spcv_replyText')
            # for button in n_replies_buttons:
            #     button.click()
            #     # Wait for the next set of replies to load
            #     WebDriverWait(self.browser, 10).until(EC.staleness_of(button))
            #     self.click_show_more_buttons()  # Recursively click on "Show more" buttons

        except Exception as e:
            print(f"An error occurred: {e}")


browser = Browser(0).getBrowser()
scraper = FoxNewsChatgpt(browser=browser, depth=5)

url = "https://www.foxnews.com/entertainment/paulina-porizkova-58-poses-topless-painted-silver-makes-me-feel-strong?dicbo=v2-M8dSAZh"
posts = scraper.check_element_exists(url)
