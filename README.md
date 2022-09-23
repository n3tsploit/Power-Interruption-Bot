<h1 align="center">Power Interruption Bot</h1>
This python telegram bot displays locations in 🇰🇪  where power outages are expected to occur in the near future.

## Functionality
Once a week, the bot parses the KPLC website and gets the most recent PDF with a list of the places that will be affected by the scheduled power outage.

Following that, data is extracted from the pdf and saved to a text file.

Unneeded information is eliminated from the text file, and the remaining information is formatted as a nested dictionary and saved to Redis.
The code contains the specifics of how everything functions.

## Important Packages Used
- [Python-telegram-bot](https://pypi.org/project/python-telegram-bot/) --> An interface to interact with the python API.
- [Regex module](https://pypi.org/project/regex/) --> Mahorly used to remove unnecesary text from the data extracted from the pdf.
- [Textract](https://textract.readthedocs.io/en/stable/) --> Extracts data from the pdf doenloaded. 
- Redis --> saves the nested dictionary.
- [Boutiful Soup](https://pypi.org/project/beautifulsoup4/) --> parses the kplc website and doenloads the latest pdf.

## How To Install Locally

- Create a folder to store the code
- At the terminal clone the repo `git clone https://github.com/n3tsploit/PowerOutage-Bot.git` or download the zip file of the code.
- inside the telebot folder create a .env file containing the API token of the telegram bot gotten from Bot father.
- start the bot by running the run.py file.

## How To Use The Bot
You can get a working prototype of the bot here https://t.me/planned_power_outage_bot .

## Demo

<iframe width="560" height="315" src="https://www.loom.com/share/866e866f1f1d41019492f75e752f8651" frameborder="0" allowfullscreen></iframe></iframe>

## Features to add
- [ ] Add an alert feature in which users will be notified if there is power interruption schduled in their county.

*PS:Built for educational purposes, and it might contain outdated/erroneous information.*



