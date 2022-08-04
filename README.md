# Power Interruption Bot
This is a python telegram bot that shows you areas in 🇰🇪 that are scheduled for power interruption within a certain period of time.

---
## How it works
The bot parses the KPLC website once per week and downloads the latest pdf containing detained of areas to be affected by the planned power interruption.
It then extracts data from the pdf and saves it to a text file.Unneccesary details are removed from the text file and the rest of the data is formated into a nested dictionary which is saved to a binary shelve file for easy access.
Fine details of how everything works is in the code.
---
## Important Packages Used
- [Python-telegram-bot](https://pypi.org/project/python-telegram-bot/) --> An interface to interact with the python API.
- [Regex module](https://pypi.org/project/regex/) --> Mahorly used to remove unnecesary text from the data extracted from the pdf.
- [Textract](https://textract.readthedocs.io/en/stable/) --> Extracts data from the pdf doenloaded. 
- [Shelve module](https://docs.python.org/3/library/shelve.html) --> saves the nested dictionary.
- [Boutiful Soup](https://pypi.org/project/beautifulsoup4/) --> parses the kplc website and doenloads the latest pdf.

---
## How To Use The Bot

---
## How To Install Locally

- Create a folder to store the code
- At the terminal clone the repo `git clone https://github.com/n3tsploit/PowerOutage-Bot.git` or download the zip file of the code.
- inside the telebot folder create a .env file containing the API token of the telegram bot gotten from Bot father.
- start the bot by running the run.py file.
- In app.py file line 29, you can change the frequency in which the bot checks for updates in the kplc website.
- 


