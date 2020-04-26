import os

from selenium import webdriver

"""
Opens a web browser through Selenium and navigates through the Algebraix
inbox, for each message creating a folder in ~/Downloads/ named after the
sender and saving all attachments in it.
Inputs: none.
Returns: nothing.
"""


def openWebBrowser():
    """
    Opens the web browser and go to the Algebraix homepage.
    Inputs: none.
    Returns: none.
    """
    print("Opening web browser …")
    browser = webdriver.Firefox()
    browser.get('https://c1-liceodelvalle.algebraix.com/')
    print("Web browser open. Please, manually log into Algebraix.")
    return browser


def getSenderName(browser):
    """
    Finds and returns sender’s name.
    Inputs: none.
    Returns: a string.
    """
    return browser.find_element_by_class_name(
        'material-card__text--primary').text
