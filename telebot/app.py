from telegram.ext import *
from telegram import *
import functions
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(".env"))
TOKEN = os.getenv('bot_token')

print('Bot is starting')

County, Area, Place = range(3)
global county_value


def start_command(update, context):
    update.message.reply_text('Welcome')
    inline_keyboard = [[InlineKeyboardButton(text="Mombasa", callback_data="Mombasa "),
                        InlineKeyboardButton(text="Kwale", callback_data="Kwale "),
                        InlineKeyboardButton(text="Kilifi", callback_data="Kilifi ")],
                       [InlineKeyboardButton(text="TanaRiver", callback_data="TanaRiver "),
                        InlineKeyboardButton(text="Lamu", callback_data="Lamu "),
                        InlineKeyboardButton(text="Taita-Taveta", callback_data="Taita-Taveta ")],
                       [InlineKeyboardButton(text="Garissa", callback_data="Garissa "),
                        InlineKeyboardButton(text="Wajir", callback_data="Wajir "),
                        InlineKeyboardButton(text="Mandera", callback_data="Mandera ")],
                       [InlineKeyboardButton(text="Marsabit", callback_data="Marsabit "),
                        InlineKeyboardButton(text="Isiolo", callback_data="Isiolo "),
                        InlineKeyboardButton(text="Meru22", callback_data="Meru22 ")],
                       [InlineKeyboardButton(text="Tharaka-Nithi", callback_data="Tharaka-Nithi "),
                        InlineKeyboardButton(text="Embu", callback_data="Embu "),
                        InlineKeyboardButton(text="Kitui", callback_data="Kitui ")],
                       [InlineKeyboardButton(text="Machakos", callback_data="Machakos "),
                        InlineKeyboardButton(text="Makueni", callback_data="Makueni "),
                        InlineKeyboardButton(text="Nyandarua", callback_data="Nyandarua ")],
                       [InlineKeyboardButton(text="Nyeri", callback_data="Nyeri "),
                        InlineKeyboardButton(text="Kirinyaga", callback_data="Kirinyaga "),
                        InlineKeyboardButton(text="Murang’a", callback_data="Murang’a ")],
                       [InlineKeyboardButton(text="Kiambu", callback_data="Kiambu "),
                        InlineKeyboardButton(text="Turkana", callback_data="Turkana "),
                        InlineKeyboardButton(text="WestPokot", callback_data="WestPokot ")],
                       [InlineKeyboardButton(text="Samburu", callback_data="Samburu "),
                        InlineKeyboardButton(text="TransNzoia", callback_data="TransNzoia "),
                        InlineKeyboardButton(text="UasinGishu", callback_data="UasinGishu ")],
                       [InlineKeyboardButton(text="Elgeyo-Marakwet", callback_data="Elgeyo-Marakwet "),
                        InlineKeyboardButton(text="Nandi", callback_data="Nandi "),
                        InlineKeyboardButton(text="Baringo", callback_data="Baringo ")],
                       [InlineKeyboardButton(text="Laikipia", callback_data="Laikipia "),
                        InlineKeyboardButton(text="Nakuru", callback_data="Nakuru "),
                        InlineKeyboardButton(text="Narok", callback_data="Narok ")],
                       [InlineKeyboardButton(text="Kajiado", callback_data="Kajiado "),
                        InlineKeyboardButton(text="Kericho", callback_data="Kericho "),
                        InlineKeyboardButton(text="Bomet", callback_data="Bomet ")],
                       [InlineKeyboardButton(text="Kakamega", callback_data="Kakamega "),
                        InlineKeyboardButton(text="Vihiga", callback_data="Vihiga "),
                        InlineKeyboardButton(text="Bungoma", callback_data="Bungoma ")],
                       [InlineKeyboardButton(text="Busia", callback_data="Busia "),
                        InlineKeyboardButton(text="Siaya", callback_data="Siaya "),
                        InlineKeyboardButton(text="Kisumu", callback_data="Kisumu ")],
                       [InlineKeyboardButton(text="HomaBay", callback_data="HomaBay "),
                        InlineKeyboardButton(text="Migori", callback_data="Migori "),
                        InlineKeyboardButton(text="Kisii", callback_data="Kisii ")],
                       [InlineKeyboardButton(text="Nyamira", callback_data="Nyamira "),
                        InlineKeyboardButton(text="Nairobi", callback_data="Nairobi ")]]

    reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Choose a  You want to check power interruption details:    ",
                              reply_markup=reply_keyboard_markup)
    return Area


def area(update, context):
    query = update.callback_query
    query.answer()
    global county_value
    county_value = query.data
    data = functions.area_list(county_value)
    print(f'This is the{data}')
    inline_keyboard = []
    for i in data:
        inline_keyboard.append(InlineKeyboardButton(i, callback_data=i))

    print(inline_keyboard[0])
    reply_keyboard_markup = InlineKeyboardMarkup([inline_keyboard])
    query.edit_message_text(text="Choose a Area ", reply_markup=reply_keyboard_markup)
    return Place


def place(update, context):
    query = update.callback_query
    query.answer()
    time_out= functions.place_list(area=query.data, county=county_value)
    print(county_value)
    print(f'this is the{time_out}')
    # print(f'This is the {place_out}')

    return ConversationHandler.END


def help_command(update, context):
    update.message.reply_text('These are some of the commands')


def stop(update, context):
    update.message.reply_text('Bye..see you later')

    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler('help', help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            Area: [CallbackQueryHandler(area)],
            Place: [CallbackQueryHandler(place)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    disp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
