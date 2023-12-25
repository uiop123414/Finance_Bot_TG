from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime


class ButtonsFactory:
    current_datetime = datetime.now()
    buttons = {
        'type_of_report': ('10-K', '10-Q', '8-K'),
        'year_of_report': (str(current_datetime.year), str(current_datetime.year - 1), str(current_datetime.year - 2)),
        'extension_of_report': ('txt', 'htm')
    }

    @staticmethod
    def get_buttons(buttons_key):
        inline_buttons = []
        for item in ButtonsFactory.buttons[buttons_key]:
            inline_buttons.append(InlineKeyboardButton(item, callback_data=item))
        kb_client = InlineKeyboardMarkup(resize_keyboard=True)
        kb_client.row(*inline_buttons)
        return kb_client
