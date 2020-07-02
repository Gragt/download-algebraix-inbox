"""
Download all files and text from an Algebraix inbox.

User is asked to log into Algebraix and navigate to the first message
in their inbox they wish to download. Upon resuming execution, the
program will walk down through the inbox and download each message
body as well as any attachments.

Files are saved in the user’s Downloads folder under AlgebraixInbox.
Each message is saved in a directory named after sender’s name.If names
have been scraped and available in students_names.py, sender’s name will
be replaced with the student’s group and student’s name.
"""

import time

from algebraix_session import AlgebraixSession
try:
    from students_names import students_names
except ModuleNotFoundError:
    students_names = {}


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
        session.set_sender_name()
        session.replace_sender_name(students_names)
        print(f"Name: {session.senderName}.")
        session.set_group(students_names)
        print("Getting body text …")
        session.set_body_text()
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
