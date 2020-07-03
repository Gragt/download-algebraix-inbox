# download_algebraix_inbox

A program to download the content of an Algebraix inbox and save it in a directory tree.

Opens a Firefox session and goes to the Algebraix website. Pauses to let user log in manually and navigate to the inbox. User should open the first message they wish to start the run from, and press Enter to resume execution. Controls Firefox to go through the inbox, message by message, downloading attachments and placing them in a folder named after the sender.

If students’s groups and parents name have been collected in a dict, the program can substitute a parent’s name for the student’s.

All downloaded files can be found in a folder named `AlgebraixInbox` inside the user’s `Downloads` folder.

## Requirements

In order to function properly, this programs requires the following to be installed:

* [Python](https://www.python.org), 3.6 or higher.
    - The `requests`, `selenium`, and `selenium-requests` Python modules.
* [Firefox](https://www.mozilla.org/firefox/new/).
    - [geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox.

### Installing the `requests`, `selenium`, and `selenium-requests` modules

Install Python first.

#### Windows

Open Command Prompt.

(Optional: enter `python -m pip install -U pip`)

Enter `pip install requests selenium selenium-requests`

#### macOS and Linux

Open Terminal.

(Optional: enter `pip3 install -U pip`)

Enter `pip install requests selenium selenium-requests`

*Note*: if you get an error, replace `pip` by `pip3`, e.g., `pip3 install requests selenium selenium-requests`.

### Installing geckodriver

#### Windows

Extract the file to your Python directory, e.g., `C:\Python3.8`.

#### macOS

If you do not have it yet, [install Homebrew](https://brew.sh).

In Terminal, enter `brew install geckodriver`.

#### Linux

Use your package manager in Terminal, e.g., `sudo apt install firefox-geckodriver` in Ubuntu.

## Usage

Open your terminal, navigate to the folder where those two files are contained, and enter `python download.py` on Windows or `python3 download.py` on macOs and Linux.

If all is installed correctly, the program launches Firefox and opens the Algebraix main page. Log in with your username and password, then open your inbox and navigate to the *first* message you want downloaded. Go back to the terminal and press Enter to continue the execution. The program will control Firefox and go through each message, collecting the body of the message and all file attachments.

It automatically creates a folder named `AlgebraixInbox` in the current user’s `Downloads` folder, in which it will create a folder for each sender. If `students_names.py` is present, the program will attempt to substitute the sender’s name for the student’s name and corresponding group, e.g., a message from a student named Luis Miguel from group 1B will be found in `~/Downloads/AlgebraixInbox/1BLuisMiguel`. The first message from a sender will be given the number 01, the second 02, etc. The number will be affixed to file names, e.g., the body of the second message will be named 02.txt and the attached image.jpg file will be renamed 02_image.jpg.
