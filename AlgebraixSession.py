import os

from selenium import webdriver


def downloadAlgebraixInbox():
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
        browser = webdriver.Firefox()
        browser.get('https://c1-liceodelvalle.algebraix.com/')

    """
    print("Opening web browser …")
    openWebBrowser()
    print("Web browser open. Please, manually log into Algebraix.")
    print("All done.")
    """
