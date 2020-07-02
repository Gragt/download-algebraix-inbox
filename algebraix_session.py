import os
import re

from seleniumrequests import Firefox


class AlgebraixSession(object):
    """
    An Algebraix Session launches and controls a web browser with Selenium. It
    provides methods to interact with the Algebraix inbox.
    """

    def __init__(self):
        """
        Initialises the session by opening the web browser.
        """
        self.browser = Firefox()
        self.browser.get("https://c1-liceodelvalle.algebraix.com/")
        self.regex = re.compile(r"(.+\.\w{3,4}) \(\d+\.?\d+[KM]\)")

    def setSenderName(self):
        """
        Finds and sets the current message’s sender’s name as a class variable.
        Returns: nothing.
        """
        self.senderName = self.browser.find_element_by_class_name(
            "material-card__text--primary").text

    def replaceSenderName(self, names):
        """
        Checks if a name belongs to a parent and substitutes it for the
        student’s name.
        Inputs: names, a dictionary (string: [string, [strings]])
        Returns: nothing.
        """
        for student, v in names.items():
            if self.senderName in v[1]:
                self.senderName = student

    def setGroup(self, names):
        """
        Checks if name belongs to a group and sets it as a class variable.
        Sets it to an empty string if no group can be matched.
        Inputs: names, a dictionary (string: [string, [strings]])
        Returns: nothing.
        """
        self.group = names.get(self.senderName, [""])[0]

    def setBodyText(self):
        """
        Finds and sets the current message’s body text as a class variable.
        Returns: nothing.
        """
        self.bodyText = self.browser.find_element_by_class_name(
            "material-card__body--paragraph." +
            "material-card__body--respect-lines.text-break"
        ).text

    def setAttachments(self):
        """
        Finds all of the current’s message attachments and sets a list of
        their URLs as a class variable.
        Returns: nothing.
        """
        self.attachments = [
            link
            for link in self.browser.find_elements_by_tag_name("a")
            if self.regex.search(link.text)
        ]

    def createDownloadDirectory(self):
        """
        Creates a directory tree where to download files if it doesn’t already
        exists. If possible, target directory will be named with the student’s
        group first.
        Returns: nothing.
        """
        self.targetPath = os.path.expanduser(
            os.path.join(
                "~", "Downloads", "AlgebraixInbox",
                f"{self.group}{self.senderName.replace(' ', '')}"
            )
        )
        os.makedirs(self.targetPath, exist_ok=True)

    def downloadFiles(self):
        """
        Downloads and saves the current message’s body text and image
        attachments. Appends the message number at the start of the name.
        Returns: nothing.
        """
        n = 1
        while os.path.isfile(os.path.join(self.targetPath, f"{n:02}.txt")):
            n += 1

        file = open(os.path.join(self.targetPath, f"{n:02}.txt"), "w")
        file.write(self.bodyText)
        file.close()

        for link in self.attachments:
            res = self.browser.request("GET", link.get_attribute("href"))
            res.raise_for_status()
            file = open(os.path.join(
                self.targetPath,
                f"{n:02}_{self.regex.search(link.text).group(1)}"), "wb")
            for chunk in res.iter_content(10000):
                file.write(chunk)
            file.close()

    def findNext(self):
        """
        Finds and returns the link to the next message. Returns False if it is
        the last message.
        Returns: a Selenium object or a Boolean value.
        """
        links = self.browser.find_elements_by_class_name("X_LOAD.action-item")
        for link in links:
            if link.get_attribute("data-original-title") == "Next":
                return link
        return False

    def browserClose(self):
        """
        Closes the web browser.
        Returns: nothing.
        """
        self.browser.close()
