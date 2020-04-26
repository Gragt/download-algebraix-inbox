import os

import requests
from selenium import webdriver


class AlgebraixSession(object):
    """
    Opens a web browser through Selenium and navigates through the Algebraix
    inbox, for each message creating a folder in ~/Downloads/ named after the
    sender and saving all attachments in it.
    """

    def __init__(self):
        """
        Initialises the session by opening the web browser then waits.
        """
        self.browser = webdriver.Firefox()
        self.browser.get('https://c1-liceodelvalle.algebraix.com/')

    def getSenderName(self):
        """
        Finds and returns sender’s name for current message.
        Returns: a string.
        """
        return self.browser.find_element_by_class_name(
            'material-card__text--primary').text

    def getBodyText(self):
        """
        Finds and returns the current message’s body text.
        Returns: a string.
        """
        return self.browser.find_element_by_class_name(
            'material-card__body--paragraph.' +
            'material-card__body--respect-lines.text-break'
        ).text

    def getAttachments(self):
        """
        Finds all image attachments of the current message and returns a list
        of their URLs.
        Returns: a list of strings.
        """
        return [
            link.get_attribute('href')
            for link in self.browser.find_elements_by_tag_name('a')
            if any(ext in link.text for ext in ['.jpg', '.jpeg', '.png'])
        ]
