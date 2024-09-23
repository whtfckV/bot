from aiogram import html, F
from aiogram import Router
from aiogram.types import (
    ContentType,
    ReplyKeyboardRemove,
    Message,
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from os import getenv
# import os

from bot_instance import bot
import app.keyboards as kb

load_dotenv()
LISA = getenv("LISA")
if not LISA:
    raise ValueError("Переменные окружения LISA не установлены")

# Get the absolute path of the project root
# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the absolute path to the video file
# about_path = os.path.join(project_root, "files", "price.jpeg")

about = "BAACAgIAAxkDAAIBfGbj014K73POtOAv5tOFvAgfY9IjAALrUgACecggSxiWTiNbld_kNgQ"
nahui = "BAACAgIAAxkDAAIB1mbj2veAIO0J7NWJhIRu-ma3LPewAAIyUwACecggS_8a3AIdm0F2NgQ"
dohuia = "BAACAgIAAxkDAAIB2Gbj2yR1W9yyJey-3qVn9WTgVwlaAAI0UwACecggSxCGtEEfIurzNgQ"
singing = "BAACAgIAAxkDAAICA2bj3piG8SCNhpL24j-mCy4BXxZ9AAJJUwACecggS1kHuuTLISRYNgQ"
price = "AgACAgIAAxkDAAIEpGbqec_3L3PtsCncumtnj-wjQoUQAAKk3zEb9GlZS2xkYdR5kbwKAQADAgADbQADNgQ"

router = Router()


class Form(StatesGroup):
    vocal_experience = State()
    music_goals = State()
    learning_goals = State()
    number = State()


# class Contact(StatesGroup):
#     number = State()

user_data_dict = {}
files_dict = {}


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.first_name)}!\n"
        f"Ты попал в Кудрявый Бот! 🎤✨\n\n"
        "Я здесь, чтобы помочь Лизе отсеять спам и назойливых фанатов. "
        "Давай я задам тебе пару вопросов, чтобы убедиться, что вы с Лизой отлично сработаетесь ✌🏻\n\n"
        "Ты когда-нибудь занимался вокалом? \n"
        "Расскажи о своём опыте",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.vocal_experience)


@router.message(Command("about"))
async def about_command_handler(message: Message) -> None:
    await message.answer_video(
        about,
        width=1028,
        height=1920,
        caption="Держи)",
        duration=63,
    )


@router.message(Command("video"))
async def video_command_handler(message: Message) -> None:
    await message.answer_video(
        singing,
        height=1028,
        width=1920,
        caption="Держи)",
        duration=12,
    )


@router.message(Form.vocal_experience)
async def process_vocal_experience(message: Message, state: FSMContext) -> None:
    await state.update_data(vocal_experience=message.text)
    await message.answer("Каких целей ты хочешь достичь в музыке?")
    await state.set_state(Form.music_goals)


@router.message(Form.music_goals)
async def process_music_goals(message: Message, state: FSMContext) -> None:
    await state.update_data(music_goals=message.text)
    await message.answer("Есть что-то, чему особенно мечтаешь научиться?")
    await state.set_state(Form.learning_goals)


@router.message(Form.learning_goals)
async def process_learning_goals(message: Message, state: FSMContext) -> None:
    await state.update_data(learning_goals=message.text)
    user_data = await state.get_data()
    await message.answer("Судя по всему, ты не простой человек!")

    user_data_dict[message.from_user.id] = user_data
    await state.clear()

    await message.answer("Хочешь узнать больше о Лизе?", reply_markup=kb.keyboard)


@router.message(F.text == kb.ABOUT)
async def about_handler(message: Message, state: FSMContext) -> None:
    await message.answer_video(
        about,
        width=1028,
        height=1920,
        caption="Держи)",
        duration=63,
    )

    await message.answer(
        "Лиза обожает делиться радостью и подготовила для тебя небольшой гайд по расслаблению и высвобождению энергии! 🔥"
        "Ты сможешь получить его, записавшись на ознакомительное занятие."
        # "Оставь свой номер, чтобы Лиза смогла легко связаться с тобой."
    )
    if message.contact:
        user_data_dict[message.from_user.id]["contact"] = message.contact.phone_number
    else:
        await message.answer(
            "Оставь свой номер, чтобы Лиза смогла легко связаться с тобой.",
            reply_markup=kb.share_number_keyboard,
        )
        await state.set_state(Form.number)


@router.message(F.text == kb.VIDEO)
async def video_handler(message: Message, state: FSMContext) -> None:
    await message.answer_video(
        singing,
        height=1028,
        width=1920,
        caption="Держи)",
        duration=12,
    )

    await message.answer(
        "Лиза обожает делиться радостью и подготовила для тебя небольшой гайд по расслаблению и высвобождению энергии! 🔥"
        "Ты сможешь получить его, записавшись на ознакомительное занятие."
    )

    if message.contact:
        contact_info = (
            f"Имя: {message.from_user.first_name}\nНомер телефона: {message.from_user}"
        )
        await message.answer(contact_info)
    else:
        await message.answer(
            "Оставь свой номер, чтобы Лиза смогла легко связаться с тобой.",
            reply_markup=kb.share_number_keyboard,
        )

        await state.set_state(Form.number)


# Хендлер для обработки контакта
@router.message(F.content_type == ContentType.CONTACT)
async def contact_handler(message: Message, state: FSMContext):
    await state.update_data(number=message.contact)
    user_data_dict[message.from_user.id]["contact"] = message.contact.phone_number

    await message.answer("Спасибо за контакт, теперь она не потеряет тебя")

    await message.answer(
        f"{message.from_user.first_name}, а теперь порадуй меня — запишись на ознакомительный урок вокала к Лизе и с 20% скидкой,"
        "ты ведь не из тех, кто готов упустить свой шанс?"
    )

    await message.answer(
        "Уже через 4 занятия ты заметишь реальные изменения — и услышишь их тоже! Запишемся? 😉"
    )

    await message.answer_photo(
        price, caption="Прайс", reply_markup=kb.appointment_keyboard
    )

    await message.answer(
        "Ты молодец! Желаю успехов в освоении вокала и море удовольствия от занятий! ✌🏻\n"
        "Будь уверен в себе, не сдавайся и наслаждайся процессом! 🔥",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Форматируем данные пользователя для отправки Лизе
    user_info = (
        f"Новый потенциальный ушной насильник:\n"
        f"- Имя: {message.from_user.first_name}\n"
        f"- Опыт вокала: {user_data_dict[message.from_user.id]['vocal_experience']}\n"
        f"- Музыкальные цели: {user_data_dict[message.from_user.id]['music_goals']}\n"
        f"- Цели обучения: {user_data_dict[message.from_user.id]['learning_goals']}\n"
        f"- Номер телефона: {user_data_dict[message.from_user.id]['contact']}"
        "Был бы у меня хуй, его можно было бы отсосать"
    )

    try:
        await bot.send_message(chat_id=LISA, text=user_info)
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю с ID {LISA}: {e}")
    await state.clear()


@router.message(Form.number)
async def phone_number_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)
    user_data = await state.get_data()
    await message.answer(
        "Спасибо за контакт, теперь она не потеряет тебя",
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer(
        f"{message.from_user.first_name}, а теперь порадуй меня — запишись на ознакомительный урок вокала к Лизе и с 20% скидкой,"
        "ты ведь не из тех, кто готов упустить свой шанс?"
    )

    await message.answer(
        "Уже через 4 занятия ты заметишь реальные изменения — и услышишь их тоже! Запишемся? 😉"
    )

    user_data_dict[message.from_user.id]["contact"] = user_data["number"]

    await message.answer_photo(
        price, caption="Прайс", reply_markup=kb.appointment_keyboard
    )

    await message.answer(
        "Ты молодец! Желаю успехов в освоении вокала и море удовольствия от занятий! ✌🏻\n"
        "Будь уверен в себе, не сдавайся и наслаждайся процессом! 🔥",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Форматируем данные пользователя для отправки Лизе
    user_info = (
        f"Новый потенциальный ушной насильник:\n\n"
        f"- Имя: {message.from_user.first_name}\n"
        f"- Опыт вокала: {user_data_dict[message.from_user.id]['vocal_experience']}\n"
        f"- Музыкальные цели: {user_data_dict[message.from_user.id]['music_goals']}\n"
        f"- Цели обучения: {user_data_dict[message.from_user.id]['learning_goals']}\n"
        f"- Номер телефона: {user_data_dict[message.from_user.id]['contact']}\n\n"
        "Был бы у меня хуй, его можно было бы отсосать"
    )

    try:
        await bot.send_message(chat_id=LISA, text=user_info)
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю с ID {LISA}: {e}")
    await state.clear()
