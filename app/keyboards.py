from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    # CallbackData
)

ABOUT = "Немного о Лизе"
VIDEO = "Видео-исполнение"

about_kb = [
    [
        KeyboardButton(text=ABOUT),
        KeyboardButton(text=VIDEO),
    ]
]

keyboard = ReplyKeyboardMarkup(
    keyboard=about_kb,
    resize_keyboard=True,
    input_field_placeholder="Выбери из меню",
)

share_number_button = [
    [
        KeyboardButton(text="Поделиться", request_contact=True),
        # KeyboardButton(text="Написать"),
    ]
]
share_number_keyboard = ReplyKeyboardMarkup(
    keyboard=share_number_button, resize_keyboard=True, one_time_keyboard=True
)

# class MyCallback(CallbackData, prefix="my"):
#     foo: str
#     bar: int

appointment_button = [
    [
        InlineKeyboardButton(
            text="Записаться на занятие",
            url="https://widget.easyweek.ru/chastnyy-pedagog-po-vokalu-elizaveta-kuzminyh/team/107126/101597",
        ),
    ]
]

appointment_keyboard = InlineKeyboardMarkup(inline_keyboard=appointment_button)
