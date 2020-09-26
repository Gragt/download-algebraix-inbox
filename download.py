"""
Download all files and text from an Algebraix inbox.

User is asked to log into Algebraix and navigate to the first message
in their inbox they wish to download. Upon resuming execution, the
program will walk down through the inbox and download each message
body as well as any attachments.

Files are saved in the user’s Downloads folder under AlgebraixInbox.
Each message is saved in a directory named after sender’s name.If names
have been scraped and available in names.py, sender’s name will
be replaced with the student’s group and student’s name.
"""

import os
import re
import time

from seleniumrequests import Firefox

try:
    from names import names
except ModuleNotFoundError:
    names = {}


class AlgebraixSession(object):
    """Launch an Algebraix session."""

    def __init__(self):
        """Initialise the session by opening the web browser."""
        self.browser = Firefox()
        self.browser.get("https://c1-summit.algebraix.com/")
        self.regex = re.compile(r"(.+\.\w{3,4}) \(\d+\.?\d+[KM]\)")

    def set_names(self):
        """Find and sets current message’s sender’s name."""
        self.names = [
            name.text for name in self.browser.find_elements_by_class_name(
                "material-card__text--primary")
        ]
        self.sender_name = self.names[0]

    def replace_sender_name(self, names):
        """
        Check if parent’s name can be substituted with student’s.

        Inputs: names, a dictionary of various data types.
        """
        for student, v in names.items():
            if self.sender_name in v[1]:
                self.sender_name = student

    def set_group(self, names):
        """
        Check student’s group if possible.

        Inputs: names, a dictionary of various data types.
        """
        self.group = names.get(self.sender_name, [""])[0]

    def set_bodies(self):
        """Find and set current message’s body text."""
        self.bodies = []
        for item in self.browser.find_elements_by_class_name(
            "material-card__body--paragraph." +
            "material-card__body--respect-lines.text-break"
        ):
            self.bodies.append(item.text + "\n\n")
        self.bodies[-1] = self.bodies[-1][:-3]

    def set_dates(self):
        """Find and set date and time for each message."""
        self.dates = [
            date.text for date in self.browser.find_elements_by_class_name(
                "material-card__body--title-secondary")
        ]

    def set_attachments(self):
        """Set a list of attachments for current message."""
        self.attachments = [
            link
            for link in self.browser.find_elements_by_tag_name("a")
            if self.regex.search(link.text)
        ]

    def create_download_directory(self):
        """Create download directory for current sender."""
        self.targetPath = os.path.expanduser(
            os.path.join(
                "~", "Downloads", "AlgebraixInbox",
                f"{self.group}{self.sender_name.title().replace(' ', '')}"
            )
        )
        os.makedirs(self.targetPath, exist_ok=True)

    def download_files(self):
        """Download and save current body text and attachments."""
        n = 1
        while os.path.isfile(os.path.join(self.targetPath, f"{n:02}.txt")):
            n += 1

        file = open(os.path.join(self.targetPath, f"{n:02}.txt"), "w")
        for name, date, body in zip(self.names, self.dates, self.bodies):
            file.write(name + "\n" + date + "\n" + body.title())
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

    def find_next(self):
        """
        Find and returns the link to the next message.

        Returns False if it is the last message.

        Returns: a Selenium object or a bool.
        """
        links = self.browser.find_elements_by_class_name("X_LOAD.action-item")
        for link in links:
            if link.get_attribute("data-original-title") == "Next":
                return link
        return False

    def browser_close(self):
        """Close the web browser."""
        self.browser.close()


def download_algebraix_inbox():
    """Create an Algebraix session and download inbox’s contents."""
    print("Opening web browser …")
    session = AlgebraixSession()
    print("Web browser open. Please, manually log into Algebraix.")
    input("Open the first message and press Enter to continue.")
    next = session.find_next()
    while True:
        time.sleep(1.5)
        print("Getting name …")
        session.set_names()
        session.replace_sender_name(names)
        print(f"Name: {session.sender_name.title()}.")
        session.set_group(names)
        print("Getting body text …")
        session.set_dates()
        session.set_bodies()
        print("Getting attachments …")
        session.set_attachments()
        print("Creating directories …")
        session.create_download_directory()
        print("Downloading files …")
        session.download_files()
        next = session.find_next()
        if not next:
            print("All done.")
            break
        print("Moving on to next message …")
        next.click()
    session.browser_close()


download_algebraix_inbox()
