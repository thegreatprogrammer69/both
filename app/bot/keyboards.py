from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def preview_keyboard(draft_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать", callback_data=f"publish:{draft_id}")],
            [InlineKeyboardButton(text="Отменить", callback_data=f"cancel:{draft_id}")],
        ]
    )
