import logging

import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5850762761:AAG3Job_FU06AxjI0CV79pTXcGqiRF5ujKE'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb_operations = [
    [types.KeyboardButton(text="+"), types.KeyboardButton(text="-"),
     types.KeyboardButton(text="*"), types.KeyboardButton(text="/")],
]
keyboard_operations = types.ReplyKeyboardMarkup(keyboard=kb_operations,
                                                resize_keyboard=True)


class Operation(StatesGroup):
    operation = State()
    a = State()
    b = State()


@dp.message_handler(commands=['start', 'info'])
async def send_welcome(message: types.Message):
    await Operation.operation.set()
    await bot.send_message(message.chat.id,
                           md.text('Выбери арифметическую операцию',
                                   sep='\n',
                                   ),
                           reply_markup=keyboard_operations,
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=Operation.operation)
async def process_operation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text == '+' and not message.text == '-' and not message.text == '*' and not message.text == '/':
            await bot.send_message(message.chat.id,
                                   md.text('Выбери корректную арифметическую операцию',
                                           sep='\n',
                                           ),
                                   reply_markup=keyboard_operations,
                                   parse_mode=ParseMode.MARKDOWN)
            return
        data['operation'] = message.text

    await Operation.next()
    markup = types.ReplyKeyboardRemove()
    await message.answer("Напиши первое число",
                         reply_markup=markup)


@dp.message_handler(state=Operation.a)
async def process_a(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            a = float(message.text)
            data['a'] = a
        except Exception as error:
            await bot.send_message(message.chat.id,
                                   md.text('Введите число',
                                           sep='\n',
                                           ),
                                   parse_mode=ParseMode.MARKDOWN)
            print(error)
            return

    await Operation.next()
    markup = types.ReplyKeyboardRemove()
    await message.answer("Напиши второе число",
                         reply_markup=markup)


@dp.message_handler(state=Operation.b)
async def process_b(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            b = float(message.text)
            data['b'] = b
        except Exception as error:
            print(error)
            await bot.send_message(message.chat.id,
                                   md.text('Введите число',
                                           sep='\n',
                                           ),
                                   parse_mode=ParseMode.MARKDOWN)
            return

    a = float(data['a'])
    b = float(data['b'])
    if data['operation'] == '+':
        await message.answer("Ответ: " + str(a + b))
    elif data['operation'] == '-':
        await message.answer("Ответ: " + str(a - b))
    elif data['operation'] == '*':
        await message.answer("Ответ: " + str(a * b))
    else:
        if b == 0:
            await message.answer("Невалидная операция")
        else:
            await message.answer("Ответ: " + str(a / b))
    await bot.send_message(message.chat.id,
                           md.text('Напиши /start, чтобы начать',
                                   sep='\n',
                                   ),
                           parse_mode=ParseMode.MARKDOWN)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
