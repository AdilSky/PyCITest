# FileName : baidu_test.py
# Author   : Adil
# DateTime : 2018/4/9 19:49
# SoftWare : PyCharm

import unittest,time

from selenium import webdriver

class Baidu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.url = 'https://www.hao123.com'
        cls.driver = webdriver.Chrome()
        cls.driver.get(cls.url)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(5)


    @classmethod
    def tearDownClass(cls):

        cls.driver.quit()

    def test_baidu(self):

        time.sleep(2)
        self.driver.find_element_by_id('search-input').send_keys("pyTest")




