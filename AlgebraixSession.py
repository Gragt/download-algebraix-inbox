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

    def setSenderName(self):
        """
        Finds and sets the current message’s sender’s name.
        Returns: nothing.
        """
        self.senderName = self.browser.find_element_by_class_name(
            'material-card__text--primary').text

    def setBodyText(self):
        """
        Finds and sets the current message’s body text.
        Returns: nothing.
        """
        self.bodyText = self.browser.find_element_by_class_name(
            'material-card__body--paragraph.' +
            'material-card__body--respect-lines.text-break'
        ).text

    def setAttachments(self):
        """
        Finds all of the current’s message image attachments and sets a list
        of their URLs.
        Returns: nothing.
        """
        self.attachments = [
            link.get_attribute('href')
            for link in self.browser.find_elements_by_tag_name('a')
            if any(ext in link.text for ext in ['.jpg', '.jpeg', '.png'])
        ]

    def createDownloadDirectory(self):
        """
        Checks and create a directory tree to download files if it doesn’t
        already exists.
        Inputs: name: a string.
        Returns: nothing.
        """
        self.targetPath = os.path.expanduser(
            os.path.join(
                '~', 'Downloads', 'AlgebraixInbox', self.senderName.replace(
                    " ", "")))
        os.makedirs(self.targetPath, exists_ok=True)
