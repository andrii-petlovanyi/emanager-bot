import telebot
from telebot import types
import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://user:user@elx.e2qwffh.mongodb.net/?retryWrites=true&w=majority")
db = client.test


current_db = client['user']

collection = current_db.posts
collection_offer = current_db.offers


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    start_message = f'Привіт, <b>{message.from_user.first_name}</b> 👋! \n\nЯ - <b>Helper🤖</b>, твій помічник🤓 та гід😎 в світі техніки <b>Elx</b>. Тому з радістю поділюсь з тобою всіма цікавими фішками та характеристиками по кожній із моделей🤗. Для цього достатньо лише ввести модель нижче та відправити мені👨‍💻. \n\nНу що ж, погнали?👻'
    bot.send_message(message.chat.id, start_message, parse_mode='html')


@bot.message_handler(func=lambda message: message.text == "Головна")
def command_text_add(messa):
    start_message = f'Привіт, <b>{messa.from_user.first_name}</b> 👋! \n\nЯ - <b>Helper🤖</b>, твій помічник🤓 та гід😎 в світі техніки <b>Elx</b>. Тому з радістю поділюсь з тобою всіма цікавими фішками та характеристиками по кожній із моделей🤗. Для цього достатньо лише ввести модель нижче та відправити мені👨‍💻. \n\nНу що ж, погнали?👻'
    bot.send_message(messa.chat.id, start_message, parse_mode='html')


@bot.message_handler(commands=['Додати'])
def add(message):
    add_message = 'Допоможи мені стати краще😇. Для цього вкажи відсутню модель і я одразу ж займусь її вивченням та пошуком всіх цікавих фішок🤓. \n\nПри введенні моделі використовуй символ "!" на початку слова🙏. \n\nНаприклад: <b>!EWS426BUI</b> \n\nЗрозумів?🙃 \nТоді мерщій набирай 👇'
    bot.send_message(message.chat.id, add_message, parse_mode='html')


@bot.message_handler(func=lambda message: message.text == "Додати")
def command_text_add(messa):
    add_message = bot.send_message(
        messa.chat.id, 'Допоможи мені стати краще😇. Для цього вкажи відсутню модель і я одразу ж займусь її вивченням та пошуком всіх цікавих фішок🤓. \nДавай мерщій набирай 👇', parse_mode='html')
    bot.register_next_step_handler(add_message, model_add)


def model_add(messa):

    offer = {
        'user_id': messa.from_user.id,
        'model': messa.text,
        'FirstName': messa.from_user.first_name,
        'LastName': messa.from_user.last_name,
        'Date': messa.date,
        'Username': messa.from_user.username,
        'Premium': messa.from_user.is_premium
    }

    collection_offer.insert_one(offer)

    bot.send_message(
        messa.chat.id, f'Пропозицію додано🥳! Щиро дякую тобі, <b>{messa.from_user.first_name}</b>! Ти допомогаєш мені рости та ставати ще крутішим😎! Тепер раджу тобі повернутись на <b>Головну</b>. Для цього просто скористайся кнопкою на панелі 👇', parse_mode='html')


@bot.message_handler(content_types='text')
def search(message):

    model = []
    info = []
    markup_official_link = []
    markup_manual_link = []
    photo = []

    for chanel in collection.find({'model': message.text.lower()}):
        info = chanel['info']
        model = chanel['model']
        markup_official_link = chanel['urlOff']
        markup_manual_link = chanel['urlBook']
        photo = chanel['imgUrl']

    markup = types.InlineKeyboardMarkup(row_width=1)
    off = types.InlineKeyboardButton('💎 Офф. сайт', url=markup_official_link)
    manual = types.InlineKeyboardButton('📖 Інструкція', url=markup_manual_link)
    markup.add(off, manual)

    if message.text.lower() == model:
        info2 = '\n' + info + '\n\n' + \
            'Також ти можеш переглянути товар на офіційному сайті💎 та ознайомитись з посібником користувача📖. Просто скористайся відповідними  кнопками нижче👇'
        bot.send_photo(message.chat.id, photo, caption=info2,
                       parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=1, one_time_keyboard=True)
        start = types.KeyboardButton('Головна')
        add = types.KeyboardButton('Додати')
        markup.add(start, add)
        bot.send_message(message.chat.id,
                         'Вибач, але введена тобою модель мені не знайома☹️. Перевір, будь ласка, чи коректно введено модель та спробуй ще раз🙂. Або ти можеш залишити побажанням і я обовʼязково дізнаюсь🧐 все найцікавіше та зможу поділитись з тобою цінною інформацією вже наступного разу😎. \n\nЩоб запропонувати відсутню модель просто натисни кнопку "Додати"👇',
                         parse_mode='html', reply_markup=markup)


bot.infinity_polling()
