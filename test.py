# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


class PhpBB3_Test(unittest.TestCase):
    loading_timer = 10
    username = "user"
    password = "pass"

    def setUp(self):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        # self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_add_reply(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        forum_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[1]/div/ul[2]/li[1]/dl/dt/div/a'))
        )
        forum_button.click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        links = driver.find_elements_by_class_name('topictitle')
        links[len(links) - 1].click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_content17"]/div'))
        )
        reply_button = driver.find_elements_by_class_name('reply-icon')
        reply_button[0].click()
        login_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[2]'))
        )
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        login_button.click()
        message = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="message-box"]/textarea'))
        )
        message.send_keys("Test")
        submit_button = driver.find_element_by_name('post')
        time.sleep(3)
        submit_button.click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_content17"]/div'))
        )
        all_posts = driver.find_elements_by_class_name('post')
        last_post_content = all_posts[len(all_posts) - 1].find_elements_by_class_name('content')
        assert last_post_content[0].text.encode("utf-8") == 'Test'  # Check if latest post content is "Test"

    def test_add_topic(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        forum_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[1]/div/ul[2]/li[1]/dl/dt/div/a'))
        )
        forum_button.click()
        new_topic_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[4]/div[1]/a'))
        )
        new_topic_button.click()
        login_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[2]'))
        )
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        login_button.click()
        subject = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.ID, 'subject'))
        )
        subject.send_keys('Test')
        message = driver.find_element_by_id('message')
        message.send_keys('Test')
        time.sleep(3)
        submit_button = driver.find_element_by_xpath('//*[@id="postform"]/div[2]/div/fieldset/input[4]')
        submit_button.click()
        post = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'post'))
        )
        post_content = post.find_elements_by_class_name('content')
        assert post_content[0].text.encode("utf-8") == 'Test'

    def test_delete_post(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        login_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nav-main"]/li[3]/a'))
        )
        login_button.click()
        submit_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[3]'))
        )
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit_button.click()
        forum_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[2]/div/ul[2]/li[1]/dl/dt/div/a'))
        )
        forum_button.click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        links = driver.find_elements_by_class_name('topictitle')
        time.sleep(1)
        links[len(links) - 1].click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_content17"]/div'))
        )
        all_posts = driver.find_elements_by_class_name("post")
        delete_button = all_posts[len(all_posts) - 1].find_elements_by_class_name('delete-icon')
        delete_button[0].click()
        confirm_permanently = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.ID, 'delete_permanent'))
        )
        confirm_permanently.click()
        submit_button = driver.find_element_by_xpath('//*[@id="confirm"]/div/div/fieldset[2]/input[7]')
        submit_button.click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_content17"]/div'))
        )
        actual_posts = driver.find_elements_by_class_name('post')
        assert len(all_posts) - 1 == len(actual_posts)  # Check if posts number is right

    def test_delete_topic(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        login_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nav-main"]/li[3]/a'))
        )
        login_button.click()
        submit_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[3]'))
        )
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit_button.click()
        forum_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[2]/div/ul[2]/li[1]/dl/dt/div/a'))
        )
        forum_button.click()
        time.sleep(1)
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        links = driver.find_elements_by_class_name('topictitle')
        links[0].click()
        delete_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'delete-icon'))
        )
        delete_button.click()
        confirm_permanently = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.ID, 'delete_permanent'))
        )
        confirm_permanently.click()
        submit_button = driver.find_element_by_xpath('//*[@id="confirm"]/div/div/fieldset[2]/input[7]')
        submit_button.click()
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        new_links = driver.find_elements_by_class_name('topictitle')
        assert len(new_links) == len(links) - 1  # Check if new topics number is correct

    def test_description(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        description = driver.find_element(By.XPATH, '//*[@id="site-description"]/p[1]').text.encode("utf-8")
        correct_description = 'A short text to describe your forum'
        assert description == correct_description

    def test_login(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        login_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nav-main"]/li[3]/a'))
        )
        login_button.click()
        submit_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[3]'))
        )
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit_button.click()
        username = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="username_logged_in"]/div/a/span'))
        )
        assert username.text.encode("utf-8") == self.username  # check the name of looged user

    def test_read_post(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        forum_button = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/div[1]/div/ul[2]/li/dl/dt/div/a'))
        )
        forum_button.click()
        time.sleep(1)
        WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        links = driver.find_elements_by_class_name('topictitle')
        links[len(links) - 1].click()
        topic_content = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_content17"]/div'))
        )
        sample = 'This is an example post in your phpBB3 installation'
        assert sample in topic_content.text.encode("utf-8")

    def test_search(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        search_field = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="keywords"]'))
        )
        search_field.send_keys("first")
        driver.find_element(By.XPATH, '//*[@id="search"]/fieldset/button').click()
        results = WebDriverWait(driver, self.loading_timer).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-body"]/h2'))
        )
        assert results.text.encode("utf-8") == 'Search found 1 match: first'

    def test_title(self):
        driver = self.driver
        driver.get('http://localhost/phpBB3/')
        title = driver.title.encode("utf-8")
        correct_title = 'exampleForum.com - Index page'
        assert title == correct_title


if __name__ == "__main__":
    unittest.main()
