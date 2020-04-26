import time

from AlgebraixSession import AlgebraixSession

from studentsNames import studentsNames


def downloadAlgebraixInbox():
    """
    Create a session to log into Algebraix and download inbox’s contents.
    Requires the user to log in and navigate to the first message. Closes the
    browser at the end.
    Returns: nothing.
    """
    print("Opening web browser …")
    session = AlgebraixSession()
    print("Web browser open. Please, manually log into Algebraix.")
    input("Open the first message and press Enter to continue.")
    next = session.findNext()
    while True:
        time.sleep(1.5)
        print("Getting name …")
        session.setSenderName()
        session.replaceSenderName(studentsNames)
        print(f"Name is {session.senderName}")
        print("Getting body text …")
        session.setBodyText()
        print("Getting attchments …")
        session.setAttachments()
        print("Creating directories …")
        session.createDownloadDirectory()
        print("Downloading files …")
        session.downloadFiles()
        next = session.findNext()
        if not next:
            print("All done.")
            break
        print("Moving on to next message …")
        next.click()
    session.browserClose()


downloadAlgebraixInbox()
