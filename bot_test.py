import telebot
from telebot import types
import weather
from datetime import datetime


def get_token():

    with open("bot_token.txt") as f:
        bot_TOKEN = f.read().strip()
    return bot_TOKEN


bot = telebot.TeleBot(get_token())


@bot.message_handler(commands=['start'])
def send_welcome(message):

# markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
# btn1 = types.KeyboardButton('Давай попробуем')
# btn2 = types.KeyboardButton('Не хочу')
# markup.add(btn1, btn2)
# msg = bot.send_message(message.chat.id, "Привет, я бот, который поможет тебе узнать прогноз погоды в твоем городе. "
#											"Хочешь попробовать?", reply_markup=markup)
# bot.register_next_step_handler(msg, first_choise)

	markup = types.InlineKeyboardMarkup()
	btn_yes = types.InlineKeyboardButton(text='Давай попробуем ✅', callback_data='yes')
	btn_no = types.InlineKeyboardButton(text='Не хочу ⛔', callback_data='no')
	markup.add(btn_yes, btn_no)
	user_info = f"Пользователь {message.from_user.first_name} {message.from_user.last_name}, {message.from_user.username}"
	print(user_info)
	bot.send_message(message.chat.id, 'Привет, я бот, который поможет тебе узнать прогноз погоды в твоем городе. '
									  'Хочешь попробовать?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def first_choise(call):

	if call.data == 'yes':
		markup = types.InlineKeyboardMarkup()
		btn_now = types.InlineKeyboardButton(text='Сейчас', callback_data='now')
		btn_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
		btn_tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
		btn_week = types.InlineKeyboardButton(text='На неделю', callback_data='week')
		markup.add(btn_now, btn_tomorrow, btn_week, btn_today)
		bot.send_message(call.message.chat.id, 'Какой период тебе интересен?', reply_markup=markup)

	elif call.data == 'no':
		bot.send_message(call.message.chat.id, "Ну и ладно, если передумаешь - пиши мне.")


@bot.callback_query_handler(func=lambda call: call.data in ['now', 'today', 'tomorrow', 'week'])
def choise_period(call):

	if call.data == 'now':
		msg = bot.send_message(call.message.chat.id, "Отлично, введи название города")
		bot.register_next_step_handler(msg, forecast_now)

	elif call.data == 'today':
		msg = bot.send_message(call.message.chat.id,
							   'Отлично, введи название города')
		bot.register_next_step_handler(msg, forecast_today)

	elif call.data == 'tomorrow':
		msg = bot.send_message(call.message.chat.id,
							   "Отлично, введи название города")
		bot.register_next_step_handler(msg, forecast_tomorrow)

	elif call.data == 'week':
		msg = bot.send_message(call.message.chat.id,
							   'Отлично, введи название города')
		bot.register_next_step_handler(msg, forecast_week)

	else:
		bot.send_message(call.message.chat.id, "ошибочный ввод")


def forecast_now(message):

	try:
		forecast = weather.weather_now(message.text)
		print(forecast)
		bot.send_message(message.chat.id, 'ты захотел узнать какая погода в ' + message.text)
		sms = f"В {message.text} сейчас такая погода:\n" \
			   f"  🌡  температура воздуха {forecast['temp_now']} гр,\n" \
			   f"  🌤  на небе {forecast['sky']},\n" \
			   f"  🌀  скорость ветра {forecast['wind_speed']} м/с,\n" \
			   f"  📏  атмосферное давление {forecast['pressure']} мм.рт.ст."
		bot.send_message(message.chat.id, sms)
	except:
		bot.send_message(message.chat.id, 'Ошибка связи с сервером')


def forecast_today(message):

	try:
		data = weather.weather_today(message.text)
		sms = f'В городе {message.text} сегодня ожидается следующая погода:\n\n'
		for item in data:
			sms_i = f" ********  {datetime.fromtimestamp(item['date']).strftime('%H : %M')}  ********\n" \
					f"  🌡  температура воздуха {item['temp']} гр,\n" \
					f"  🌤  на небе {item['sky']},\n" \
					f"  🌀  скорость ветра {item['wind_speed']} м/с,\n" \
					f"  📏  атмосферное давление {item['pressure']} мм.рт.ст.\n\n"
			sms += sms_i
		bot.send_message(message.chat.id, sms)
	except:
		bot.send_message(message.chat.id, 'Ошибка связи с сервером')


def forecast_tomorrow(message):

	try:
		data = weather.weather_tomorrow(message.text)
		sms = f'В городе {message.text} завтра ожидается следующая погода:\n\n'
		sms_i = f"  🌡  температура воздуха днем {data['temp_day']} гр,\n" \
					f"  🌡  температура воздуха ночью {data['temp_night']} гр,\n" \
					f"  🌤  на небе {data['sky']},\n" \
					f"  🌀  скорость ветра {data['wind_speed']} м/с,\n" \
					f"  ↔  направление ветра {data['wind_deg']},\n" \
					f"  📏  атмосферное давление {data['pressure']} мм.рт.ст.\n\n"
		sms += sms_i
		bot.send_message(message.chat.id, sms)
	except:
		bot.send_message(message.chat.id, 'Ошибка связи с сервером')


def forecast_week(message):

	try:
		data = weather.weather_for_week(message.text)
		sms = f'В городе {message.text} ожидается следующая погода:\n\n'
		for item in data:
			sms_i = f"********   {datetime.fromtimestamp(item['date']).strftime('%d-%m-%Y')}   *********\n" \
					 f"  🌡  температура воздуха днем {item['temp_day']} гр,\n" \
					 f"  🌡  температура воздуха ночью {item['temp_night']} гр,\n" \
					 f"  🌤  на небе {item['sky']},\n" \
					 f"  🌀  скорость ветра {item['wind_speed']} м/с,\n" \
					 f"  ↔  направление ветра {item['wind_deg']},\n" \
					 f"  📏  атмосферное давление {item['pressure']} мм.рт.ст.\n\n"
			sms += sms_i
		bot.send_message(message.chat.id, sms)
	except:
		bot.send_message(message.chat.id, 'Ошибка связи с сервером')


# bot.polling()
bot.infinity_polling(True)
