from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml
import time
import random


class InstaBot:
    def __init__(self, path, bin_loc, username, password):
        # Setting up the Brave driver to work with Selenium webdriver:
        options = Options()
        options.binary_location = bin_loc
        self.__driver = webdriver.Chrome(executable_path=path, chrome_options=options)

        # Defining class variables:
        self.__username = username
        self.__password = password

    def login(self):
        # Getting the Instagram login website:
        self.__driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(5)

        # Entering the credentials into input form:
        self.__driver.find_element_by_name('username').send_keys(self.__username)
        self.__driver.find_element_by_name('password').send_keys(self.__password)
        time.sleep(1)

        # Clicking the Login button:
        self.__driver.find_element_by_xpath(
            '//*[@id=\"react-root\"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        time.sleep(5)

    def select_photo(self, tag):
        # Getting the website with photos of given hashtag:
        self.__driver.get('https://www.instagram.com/explore/tags/' + tag + '/')
        time.sleep(2)

        # Clicking the first photo on the page:
        self.__driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]').click()
        time.sleep(1)

    def follow(self, tag, amount):
        self.select_photo(tag)
        for n in range(amount):
            # Clicking the Follow button:
            self.__driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

            # Getting the name of the followed person:
            followed_person = self.__driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
            print(followed_person)
            time.sleep(random.uniform(1, 3))

            # Moving on to the next photo:
            self.__driver.find_element_by_class_name('HBoOv.coreSpriteRightPaginationArrow').click()
            time.sleep(random.uniform(1, 3))

        # Deleting cookies so the account won't be blocked:
        self.__driver.delete_all_cookies()

    def like(self, tag, amount):
        self.select_photo(tag)
        for n in range(amount):
            # Clicking the Like button:
            self.__driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
            time.sleep(random.uniform(1, 3))

            # Moving on to the next photo:
            self.__driver.find_element_by_class_name('HBoOv.coreSpriteRightPaginationArrow').click()
            time.sleep(random.uniform(1, 3))

        # Deleting cookies so the account won't be blocked:
        self.__driver.delete_all_cookies()


def main():

    config_path = r'D:\GitKraken\InstaBot\config.yaml'

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

            bin_location = config['webdriver']['bin_location']
            path = config['webdriver']['path']

            username = config['credentials']['username']
            password = config['credentials']['password']

            hashtag_list = config['hashtags']

            # The number of photos to like/follow should be fairly low:
            number = config['ph_number']

            bot = InstaBot(path, bin_location, username, password)
            bot.login()
            for hashtag in hashtag_list:
                bot.like(hashtag, number)
                bot.login()

    except Exception as e:
        print('Error reading the config file')
        print(e)


if __name__ == '__main__':
    main()
