import os
import re
import sys
import time

from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys

PAGES = {
    "HOME": "http://www.seamless.com",
    "HISTORY": "https://www.seamless.com/account/history"
}


def login(browser, username, password):
    browser.get(PAGES["HOME"])
    browser.find_element_by_css_selector("li.signInLink button").click()
    browser.find_elements_by_css_selector("input[name=email]")[1].send_keys(username)
    browser.find_elements_by_css_selector("input[name=password]")[1].send_keys(password)
    browser.execute_script(
        """document.querySelectorAll('form[name="signInVm.signInForm"] div[class="s-col-xs-12"] button')[0].click()"""
    )
    time.sleep(5)


def reorder_most_recent():
    try:
        browser = webdriver.Firefox()
        browser.implicitly_wait(10)
        username = os.environ["SEAMLESS_USERNAME"]
        password = os.environ["SEAMLESS_PASSWORD"]
        login(browser, username, password)

        browser.get(PAGES["HISTORY"])
        reorder_buttons = browser.find_elements_by_css_selector(
            ".past-order-cta-button"
        )
        element_to_click = None
        # Some restaurants might be closed, find the first open one...
        button_counter = 0
        for button in reorder_buttons:
            class_text = button.get_attribute("class")
            if "disabled" not in class_text and "tertiary" not in class_text:
                button_counter += 1
                element_to_click = button
                # Can use this counter to get directly to a restaurant.
                # I needed to do that once...
                # This uses first button, but you can change it.
                if button_counter > 0:
                    break
        element_to_click.click()
        time.sleep(5)
        browser.find_element_by_css_selector(
            "#ghs-cart-checkout-button"
        ).click()
        time.sleep(5)
        browser.find_element_by_css_selector(
            "#ghs-checkout-review-submit"
        ).click()
        time.sleep(20)
    finally:
        browser.quit()

