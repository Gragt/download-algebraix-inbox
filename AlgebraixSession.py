import os

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
        Finds and returns sender’s name.
        Returns: a string.
        """
        return self.browser.find_element_by_class_name(
            'material-card__text--primary').text
