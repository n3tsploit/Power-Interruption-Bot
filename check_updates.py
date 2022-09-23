import datetime
import time
from telebot import functions


# This function periodically checks for updates in the website
def check_updates():
    print('checking')
    pdf_name = functions.parse_content()
    time.sleep(3)
    functions.extract_pdf(pdf_name)
    time.sleep(1)
    functions.clean_extracted_data()
    time.sleep(1)
    functions.save_data_to_shelve()
    print(f'Checked for updates on {datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')


if __name__ == '__main__':
    if datetime.datetime.today().weekday() == 6 or datetime.datetime.today().weekday() == 1 or datetime.datetime.today().weekday() == 4:
        check_updates()
    else:
        print('Today is not Sunday')
