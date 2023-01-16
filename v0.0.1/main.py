import telebot
from openpyexcel import load_workbook
from telebot import types


bot = telebot.TeleBot(TOKEN)
fn = './files/1.xlsx'
book = load_workbook(fn)
sheet = book['Лист1']
sheet2 = book['Лист2']




#------Головна команда старту
@bot.message_handler(commands=['start'])
def start(message):
     start_message = f'Привіт, <b>{message.from_user.first_name}</b> 👋! \n\nЯ - <b>Helper🤖</b>, твій помічник🤓 та гід😎 в світі техніки <b>Elx</b>. Тому з радістю поділюсь з тобою всіма цікавими фішками та характеристиками по кожній із моделей🤗. Для цього достатньо лише ввести модель нижче та відправити мені👨‍💻. \n\nНу що ж, погнали?👻'
     bot.send_message(message.chat.id, start_message, parse_mode='html')


#-----Команда повернення на головну, аналог старт, тільки працює з кнопки на панелі
@bot.message_handler(func=lambda message: message.text == "Головна")
def command_text_add(messa):
     start_message = f'Привіт, <b>{messa.from_user.first_name}</b> 👋! \n\nЯ - <b>Helper🤖</b>, твій помічник🤓 та гід😎 в світі техніки <b>Elx</b>. Тому з радістю поділюсь з тобою всіма цікавими фішками та характеристиками по кожній із моделей🤗. Для цього достатньо лише ввести модель нижче та відправити мені👨‍💻. \n\nНу що ж, погнали?👻'
     bot.send_message(messa.chat.id, start_message, parse_mode='html')



#-----Функція додавання в базу відсутньої моделі
# Пише клієнту та очікує на дані
@bot.message_handler(func=lambda message: message.text == "Додати")
def command_text_add(messa):
     add_message = bot.send_message(messa.chat.id, 'Допоможи мені стати краще😇. Для цього вкажи відсутню модель і я одразу ж займусь її вивченням та пошуком всіх цікавих фішок🤓. \nДавай мерщій набирай 👇', parse_mode='html')
     bot.register_next_step_handler(add_message, model_add)

#------Після отримання даних записуємо їх в змінну model та далі записуємо їх в файл. Також виводимо повідомлення про успішний запис
def model_add(messa):
     model = messa.text
     sheet2.append([model, messa.from_user.first_name, messa.from_user.last_name])
     book.save(fn)
     bot.send_message(messa.chat.id, f'Пропозицію додано🥳! Щиро дякую тобі, <b>{messa.from_user.first_name}</b>! Ти допомогаєш мені рости та ставати ще крутішим😎! Тепер ти можеш повернутись на <b>Головну</b> (кнопка на панелі), або ж вводь наступну модель для пошуку 👇', parse_mode='html')


#-----Основна функція пошуку та виведення інформації про модель
@bot.message_handler(content_types='text')
def search(message):
     info = []
     model = []
     markup_official_link = []
     markup_manual_link = []

     for i in range(2, sheet.max_row+1):
          if message.text.lower() == sheet[i][0].value:
               info = sheet[i][1].value
               model = sheet[i][0].value
               markup_official_link = sheet[i][2].value
               markup_manual_link = sheet[i][3].value
               photo = sheet[i][4].value

     #------Наші інлайнові кнопки під постом з посиланнями
     markup = types.InlineKeyboardMarkup(row_width=1)
     off = types.InlineKeyboardButton('💎 Офф. сайт', url=markup_official_link)
     manual = types.InlineKeyboardButton('📖 Інструкція', url=markup_manual_link)
     markup.add(off, manual)

     if message.text.lower() == model:
          info2 = '\n' + info + '\n\n' + 'Також ти можеш переглянути товар на офіційному сайті💎 та ознайомитись з посібником користувача📖. Просто скористайся відповідними  кнопками нижче👇'
          bot.send_photo(message.chat.id, open(photo, 'rb'), caption=info2, parse_mode='html', reply_markup=markup)

          

     else:
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
          start = types.KeyboardButton('Головна')
          add = types.KeyboardButton('Додати')
          markup.add(start, add)
          bot.send_message(message.chat.id, 'Вибач, але введена тобою модель мені не знайома☹️. Перевір, будь ласка, чи коректно введено модель та спробуй ще раз🙂. Або ти можеш залишити побажанням і я обовʼязково дізнаюсь🧐 все найцікавіше та зможу поділитись з тобою цінною інформацією вже наступного разу😎. \n\nЩоб запропонувати відсутню модель просто натисни кнопку "Додати"👇', parse_mode='html', reply_markup=markup)


bot.infinity_polling()