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


def start_command(update, context):
    update.message.reply_text('Welcome')
    inline_keyboard = [[InlineKeyboardButton(text="Mombasa", callback_data="Mombasa county"),
                        InlineKeyboardButton(text="Kwale", callback_data="Kwale county"),
                        InlineKeyboardButton(text="Kilifi", callback_data="Kilifi county")],
                       [InlineKeyboardButton(text="TanaRiver", callback_data="TanaRiver county"),
                        InlineKeyboardButton(text="Lamu", callback_data="Lamu county"),
                        InlineKeyboardButton(text="Taita-Taveta", callback_data="Taita-Taveta county")],
                       [InlineKeyboardButton(text="Garissa", callback_data="Garissa county"),
                        InlineKeyboardButton(text="Wajir", callback_data="Wajir county"),
                        InlineKeyboardButton(text="Mandera", callback_data="Mandera county")],
                       [InlineKeyboardButton(text="Marsabit", callback_data="Marsabit county"),
                        InlineKeyboardButton(text="Isiolo", callback_data="Isiolo county"),
                        InlineKeyboardButton(text="Meru22", callback_data="Meru22 county")],
                       [InlineKeyboardButton(text="Tharaka-Nithi", callback_data="Tharaka-Nithi county"),
                        InlineKeyboardButton(text="Embu", callback_data="Embu county"),
                        InlineKeyboardButton(text="Kitui", callback_data="Kitui county")],
                       [InlineKeyboardButton(text="Machakos", callback_data="Machakos county"),
                        InlineKeyboardButton(text="Makueni", callback_data="Makueni county"),
                        InlineKeyboardButton(text="Nyandarua", callback_data="Nyandarua county")],
                       [InlineKeyboardButton(text="Nyeri", callback_data="Nyeri county"),
                        InlineKeyboardButton(text="Kirinyaga", callback_data="Kirinyaga county"),
                        InlineKeyboardButton(text="Murang’a", callback_data="Murang’a county")],
                       [InlineKeyboardButton(text="Kiambu", callback_data="Kiambu county"),
                        InlineKeyboardButton(text="Turkana", callback_data="Turkana county"),
                        InlineKeyboardButton(text="WestPokot", callback_data="WestPokot county")],
                       [InlineKeyboardButton(text="Samburu", callback_data="Samburu county"),
                        InlineKeyboardButton(text="TransNzoia", callback_data="TransNzoia county"),
                        InlineKeyboardButton(text="UasinGishu", callback_data="UasinGishu county")],
                       [InlineKeyboardButton(text="Elgeyo-Marakwet", callback_data="Elgeyo-Marakwet county"),
                        InlineKeyboardButton(text="Nandi", callback_data="Nandi county"),
                        InlineKeyboardButton(text="Baringo", callback_data="Baringo county")],
                       [InlineKeyboardButton(text="Laikipia", callback_data="Laikipia county"),
                        InlineKeyboardButton(text="Nakuru", callback_data="Nakuru county"),
                        InlineKeyboardButton(text="Narok", callback_data="Narok county")],
                       [InlineKeyboardButton(text="Kajiado", callback_data="Kajiado county"),
                        InlineKeyboardButton(text="Kericho", callback_data="Kericho county"),
                        InlineKeyboardButton(text="Bomet", callback_data="Bomet county")],
                       [InlineKeyboardButton(text="Kakamega", callback_data="Kakamega county"),
                        InlineKeyboardButton(text="Vihiga", callback_data="Vihiga county"),
                        InlineKeyboardButton(text="Bungoma", callback_data="Bungoma county")],
                       [InlineKeyboardButton(text="Busia", callback_data="Busia county"),
                        InlineKeyboardButton(text="Siaya", callback_data="Siaya county"),
                        InlineKeyboardButton(text="Kisumu", callback_data="Kisumu county")],
                       [InlineKeyboardButton(text="HomaBay", callback_data="HomaBay county"),
                        InlineKeyboardButton(text="Migori", callback_data="Migori county"),
                        InlineKeyboardButton(text="Kisii", callback_data="Kisii county")],
                       [InlineKeyboardButton(text="Nyamira", callback_data="Nyamira county"),
                        InlineKeyboardButton(text="Nairobi", callback_data="Nairobi county")]]

    reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Choose a county You want to check power interruption details:    ",
                              reply_markup=reply_keyboard_markup)
    return County


def county(update, context):
    query = update.callback_query
    query.answer()
    print(f'this is the{query.data}')
    data = functions.place_list(query.data)
    print(f'This is the{data}')
    inline_keyboard = []
    for i in data:
        inline_keyboard.append(InlineKeyboardButton(i, callback_data=i))

    print(inline_keyboard[0])
    reply_keyboard_markup = InlineKeyboardMarkup([inline_keyboard])
    query.edit_message_text(text="Choose a Place ", reply_markup=reply_keyboard_markup)
    return Place


def place(update, context):
    query = update.callback_query
    query.answer()
    data = functions.area_list(query.data)
    print(f'this is the{data}')
    inline_keyboard = []
    for i in data:
        inline_keyboard.append(InlineKeyboardButton(f'{i}', callback_data=f'{i}'))

    reply_keyboard_markup = InlineKeyboardMarkup([inline_keyboard])
    query.edit_message_text(text="Choose an area:", reply_markup=reply_keyboard_markup)
    return Area


def area(update, context):
    query = update.callback_query
    query.answer()
    print(f'this is the{query.data}')
    data = functions.specific(query.data)
    print(f'this is the{data}')
    query.edit_message_text(text=data)

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
            County: [CallbackQueryHandler(county)],
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
