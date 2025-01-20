from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from asyncio import CancelledError, create_task
from app.generators import generate
from app.keyboards import main_keyboard, cancel_keyboard
from app.states import Chat
from app.database.requests import set_user
user = Router()
active_tasks = {}
@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(
        '👾 Приветствую! Я Mr. Robot — ваш персональный помощник с искусственным интеллектом. '
        'Я здесь, чтобы помочь вам с любыми задачами: от ответов на вопросы до выполнения сложных вычислений',
        reply_markup=main_keyboard
    )
@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer(
        "Введите ваш запрос или нажмите 'Отменить запрос', чтобы вернуться в меню.",
        reply_markup=cancel_keyboard
    )
@user.message(Chat.text)
async def ai(message: Message, state: FSMContext):
    await state.set_state(Chat.wait)
    await message.answer("Ваш запрос обрабатывается. Подождите немного...", reply_markup=cancel_keyboard)
    task = create_task(handle_generation(message, state))
    active_tasks[message.from_user.id] = task
async def handle_generation(message: Message, state: FSMContext):
    try:
        res = await generate(message.text)
        await message.answer(res.choices[0].message.content, reply_markup=main_keyboard)
    except CancelledError:
        await message.answer("Запрос был отменен.", reply_markup=main_keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=main_keyboard)
    finally:
        active_tasks.pop(message.from_user.id, None)
        await state.clear()
@user.message(F.text == "Отменить запрос")
async def cancel_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task = active_tasks.get(user_id)

    if task:
        task.cancel()
        active_tasks.pop(user_id, None)
    await state.clear()
    await message.answer(
        "Запрос отменен. Вы можете вернуться в главное меню.",
        reply_markup=main_keyboard
    )
@user.message(Chat.wait)
async def ignore_while_processing(message: Message):
    await message.answer("Подождите! Запрос еще обрабатывается или нажмите 'Отменить запрос'.")

