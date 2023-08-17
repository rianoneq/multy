
import re
import logging
from aiogram import Bot, Dispatcher, executor, types
import json
import datetime
import sys
from .count_distance import find_nearest_couriers
# sys.path.append('../database')
from database import db


token = '5327457313:AAFkbRmO_ZpBFNfzBCMHWCnE3UzsmrREoec'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)
db = db()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(f'Добро пожаловать!\nДанный бот поможет вам найти ближайших к вам курьеров.'
                         f'Для этого просто отправьте zip код данному боту.\nА дальше мы все сделаем сами.\n'
                         f'Приятного использования!)')

""" команда для показа кол-ва курьеров в бд """
@dp.message_handler(commands=['count_couriers'])
async def send_welcome(message: types.Message):
    couries_count = db.get_couriers_count_in_db()
    await message.answer(f'Количество курьеров на данный момент в базе: <code>{couries_count}</code>', parse_mode="HTML")

""" 
    команда для показа успешности парсинга каждого из сайтов доноров 
    построчно считывает файл data/statuses, если статус FAILED, выделяет его, чтобы его было лучше видно 
"""
@dp.message_handler(commands=['statuses'])
async def send_welcome(message: types.Message):
    with open(r'../data/statuses.txt', 'r', encoding='utf8') as f:
        services = f.readlines()
        message_ = '<i>Статусы служб</i>:\n\n'
        for service in services:
            if 'FAILED' in service:
                message_ += f"{service.replace('FAILED', '').strip()} <code>FAILED</code>\n"
            else:
                message_ += service
    await bot.send_message(message.from_user.id, message_, parse_mode="HTML")


@dp.message_handler()
async def message_handler(message):
    """ проверка, подписан ли пользователь на канал """ 
    user_channel_status = await bot.get_chat_member(chat_id='@FindDropNews', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        couriers_ = db.get_couriers()

        """ загрузка зип кодов сша """ 
        with open(r"data/zip_codes_usa.json", "r") as f:
            zip_codes_4 = json.load(f)
        print(datetime.datetime.now(), "MESSAGE", message.from_user.username, message.text)

        telegram_id = message.chat.id
        
        """ проверка на то, является ли сообщение зип кодом """ 
        zip_code_maybe = re.findall(r"\d{5}", message.text)
        if len(zip_code_maybe) == 1 or len(message.text) != 5:
            try:
                user_zip_code = message.text
                
                user_zip_code_info = zip_codes_4[message.text]
                if not user_zip_code_info:
                    raise KeyError
                
                """ 
                    если является то функцией из count_couriers.py получает отфильтрованный список 
                    ближайших к введоному коду курьеров и выдает их, (с переводом километры в мили)
                """ 
                nearest_couriers = find_nearest_couriers(zip_code_sf=user_zip_code, zip_codes_4=zip_codes_4, couriers_=couriers_)
                nearest_couriers_len = len(nearest_couriers)
                text = "<i>Ближайшие курьеры:</i>\n" \
                    "\n"
                for i in range(nearest_couriers_len):
                    if i > 19:
                        break
                    courier_info = nearest_couriers[i]

                    text = text + f"{i + 1}. <code>{round(courier_info['distance'] * 0.621371, 1)} miles\n" \
                                f"Address: {courier_info['town']} | {courier_info['state']} | {courier_info['zip_code']}\n" \
                                f"Expired: {courier_info['expired']}\n" \
                                f"Status: {courier_info['status']}\n" \
                                f"Service: {courier_info['service']}</code>\n" \
                                f"\n"

                await bot.send_message(telegram_id, text=text, parse_mode="HTML")
            except KeyError:
                await bot.send_message(telegram_id, text="Индекса нет в базе данных")
        else:
            await bot.send_message(telegram_id, text="Это не почтовый индекс")
    else:
     await bot.send_message(message.from_user.id, 'Чтобы пользоваться ботом подпишись на канал @FindDropNews')
    



# if __name__ == '__main__':
executor.start_polling(dp, skip_updates=True)
