import telegram
from telegram.ext import *
from telegram import *
from telebot import functions
from dotenv import load_dotenv
import os
from pathlib import Path
import shelve

# url = functions.parse_content()
# functions.extract_pdf(url)
# functions.clean_extracted_data()
# functions.save_data_to_shelve()
shelve_file = shelve.open('telebot/content/data_file')
regions = shelve_file['regions']

load_dotenv(Path("./telebot/.env"))
TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', 88))

print('Bot is starting')

County, Area, Place = range(3)
global county_value
global area_value


def start_command(update,context):
    update.message.reply_text(f'Greetings {update.message.from_user.first_name}\U0001F601\n\nThis is an unofficial bot '
                              f'which shows you Planned Power Interruptions in 🇰🇪.\n\nCommands are as follows:-'
                              f'\n\U0001F4A1/check - To check the areas Planned for '
                              f'Interruptions.\n\U0001F4A1/pdf - To download a pdf of areas listed for Planned '
                              f'Interruptions.\n\U0001F4A1/info - To get information about the bot.'
                              f'\n\U0001F4A1/stop - To exit the conversion.')


def check_command(update, context):
    inline_keyboard = [[InlineKeyboardButton(text="Baringo", callback_data="Baringo"),
                        InlineKeyboardButton(text="Bomet", callback_data="Bomet"),
                        InlineKeyboardButton(text="Bungoma", callback_data="Bungoma")],
                       [InlineKeyboardButton(text="Busia", callback_data="Busia"),
                        InlineKeyboardButton(text="Elgeyo-Marakwet", callback_data="Elgeyo-Marakwet"),
                        InlineKeyboardButton(text="Embu", callback_data="Embu")], [
                           InlineKeyboardButton(text="Garissa", callback_data="Garissa"),
                           InlineKeyboardButton(text="HomaBay", callback_data="HomaBay"),
                           InlineKeyboardButton(text="Isiolo", callback_data="Isiolo")], [
                           InlineKeyboardButton(text="Kajiado", callback_data="Kajiado"),
                           InlineKeyboardButton(text="Kakamega", callback_data="Kakamega"),
                           InlineKeyboardButton(text="Kericho", callback_data="Kericho")], [
                           InlineKeyboardButton(text="Kiambu", callback_data="Kiambu"),
                           InlineKeyboardButton(text="Kilifi", callback_data="Kilifi"),
                           InlineKeyboardButton(text="Kirinyaga", callback_data="Kirinyaga")], [
                           InlineKeyboardButton(text="Kisii", callback_data="Kisii"),
                           InlineKeyboardButton(text="Kisumu", callback_data="Kisumu"),
                           InlineKeyboardButton(text="Kitui", callback_data="Kitui")], [
                           InlineKeyboardButton(text="Kwale", callback_data="Kwale"),
                           InlineKeyboardButton(text="Laikipia", callback_data="Laikipia"),
                           InlineKeyboardButton(text="Lamu", callback_data="Lamu")], [
                           InlineKeyboardButton(text="Machakos", callback_data="Machakos"),
                           InlineKeyboardButton(text="Makueni", callback_data="Makueni"),
                           InlineKeyboardButton(text="Mandera", callback_data="Mandera")], [
                           InlineKeyboardButton(text="Marsabit", callback_data="Marsabit"),
                           InlineKeyboardButton(text="Meru", callback_data="Meru"),
                           InlineKeyboardButton(text="Migori", callback_data="Migori")], [
                           InlineKeyboardButton(text="Mombasa", callback_data="Mombasa"),
                           InlineKeyboardButton(text="Murang’a", callback_data="Murang’a"),
                           InlineKeyboardButton(text="Nairobi", callback_data="Nairobi")], [
                           InlineKeyboardButton(text="Nakuru", callback_data="Nakuru"),
                           InlineKeyboardButton(text="Nandi", callback_data="Nandi"),
                           InlineKeyboardButton(text="Narok", callback_data="Narok")], [
                           InlineKeyboardButton(text="Nyamira", callback_data="Nyamira"),
                           InlineKeyboardButton(text="Nyandarua", callback_data="Nyandarua"),
                           InlineKeyboardButton(text="Nyeri", callback_data="Nyeri")], [
                           InlineKeyboardButton(text="Samburu", callback_data="Samburu"),
                           InlineKeyboardButton(text="Siaya", callback_data="Siaya"),
                           InlineKeyboardButton(text="Taita-Taveta", callback_data="Taita-Taveta")], [
                           InlineKeyboardButton(text="TanaRiver", callback_data="TanaRiver"),
                           InlineKeyboardButton(text="Tharaka-Nithi", callback_data="Tharaka-Nithi"),
                           InlineKeyboardButton(text="TransNzoia", callback_data="TransNzoia")], [
                           InlineKeyboardButton(text="Turkana", callback_data="Turkana"),
                           InlineKeyboardButton(text="UasinGishu", callback_data="UasinGishu"),
                           InlineKeyboardButton(text="Vihiga", callback_data="Vihiga")], [
                           InlineKeyboardButton(text="Wajir", callback_data="Wajir"),
                           InlineKeyboardButton(text="WestPokot", callback_data="WestPokot")]]

    reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Select your County:",
                              reply_markup=reply_keyboard_markup)
    return Area


def area(update, context):
    query = update.callback_query
    query.answer()
    global county_value
    county_value = query.data
    print(county_value)
    data = functions.area_list(county=county_value, regions=regions)
    if data is None:
        query.edit_message_text('No Planned Power Interruptions in this County!\nExiting...')
        return ConversationHandler.END
    inline_keyboard = []
    for i in data:
        inline_keyboard.append(InlineKeyboardButton(text=str(i), callback_data=str(i)))

    reply_keyboard_markup = InlineKeyboardMarkup([inline_keyboard[i:i + 1] for i in range(0, len(inline_keyboard), 1)])
    query.edit_message_text('--fetching--')
    query.edit_message_text(text="Select your area if it is listed below to get more details.\n"
                                 "If not,then there isn't Planned Interruptions in your area.Click /stop to exit.",
                            reply_markup=reply_keyboard_markup)
    return Place


def place(update, context):
    query = update.callback_query
    query.answer()
    place_value, time_value = functions.place_list(area=query.data, county=county_value, regions=regions)
    place_value = '\n▪️'.join(place_value)
    place_value = '<b>📅'+time_value + '\n' + '-' * 49 + '\n' + 'Specific places to be affected are:</b>\n▪️' + place_value
    query.edit_message_text('--fetching--')
    query.edit_message_text(place_value,parse_mode=telegram.ParseMode.HTML)

    context.bot.sendMessage(text='Bye👋', chat_id=update.effective_chat.id)
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text('Bye..see you later👋')

    return ConversationHandler.END


def unknown(update, context):
    update.message.reply_text('Sorry I cannot understand the text!🥲')


def main():
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler('info', start_command))
    disp.add_handler(CommandHandler('start', start_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('check', check_command)],
        states={
            Area: [CallbackQueryHandler(area)],
            Place: [CallbackQueryHandler(place)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    disp.add_handler(conv_handler)

    disp.add_handler(MessageHandler(Filters.text, unknown))

    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN,
    #                       webhook_url='https://powerinterruption.herokuapp.com/' + TOKEN)
    updater.start_polling()

    updater.idle()
