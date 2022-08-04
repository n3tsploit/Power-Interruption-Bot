# Power Interruption Bot
This is a python telegram bot that shows you areas in 🇰🇪 that are scheduled for power interruption within a certain period of time.

## How it works

The bot parses the KPLC website once per week and downloads the latest pdf containing detained of areas to be affected by the planned power interruption.
It then extracts data from the pdf and saves it to a text file.Unneccesary details are removed from the text file and the rest of the data is formated into a nested dictionary which is saved to a binary shelve file for easy access.
Fine details of how everything works is in the code.

## Important Packages Used
Python-telegram-bot\
Regex module\
Textract\
Shelve module\
Boutiful Soup


