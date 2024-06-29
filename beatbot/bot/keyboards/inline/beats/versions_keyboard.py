import os
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_versions_keyboard(beats_dict: dict, model: str, session_dir: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()

    for key, file_path in sorted(beats_dict.items(), key=lambda x: int(x[0])):
        file = os.path.basename(file_path)
        kb.button(
            text=key,
            callback_data=f"beat:{model}:{session_dir}:{file}",
        )

    kb.adjust(3)  # Adjust to 3 buttons per row

    return kb.as_markup()
