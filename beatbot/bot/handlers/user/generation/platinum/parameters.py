import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.middlewares import UserDataMiddleware
from bot.database.methods.get import get_user_credits
from bot.states.generation import Platinum
from bot.keyboards.inline.beats.platinum import *
from bot.web.requests.Service import beat_req
from bot.misc import create_user_dir, parameters

platinum_router = Router()

platinum_router.callback_query.outer_middleware(UserDataMiddleware())


@platinum_router.callback_query(F.data == 'generation:platinum')
async def choose_style(c: CallbackQuery,
                       state: FSMContext,
                       user):
    await state.set_state(Platinum.style)
    await c.message.edit_text(f'Выберите стиль', reply_markup=await styles_markup('platinum'))


@platinum_router.callback_query(Platinum.style)
async def choose_bpm(c: CallbackQuery,
                     state: FSMContext,
                     user):
    c_data = c.data.split(':')
    await state.update_data(style=c_data[0],
                            min_bpm=c_data[1],
                            max_bpm=c_data[3])

    await state.set_state(Platinum.bpm)
    await c.message.edit_text(f'Выберите bpm', reply_markup=await bpm_markup(int(c_data[2])))


@platinum_router.callback_query(Platinum.bpm)
async def choose_lad(c: CallbackQuery,
                     state: FSMContext,
                     user):
    data = await state.get_data()

    c_data = c.data.split(':')

    if c_data[0] == 'submit':
        await state.update_data(bpm=c_data[1])
        await state.set_state(Platinum.lad)
        await c.message.edit_text(f'Выберите лад', reply_markup=KB_LAD)
        return

    bpm = int(c_data[1]) + int(c_data[2])
    min_bpm = int(data['min_bpm'])
    max_bpm = int(data['max_bpm'])

    if min_bpm <= bpm <= max_bpm:
        await c.message.edit_text(f'Ваш bpm: {bpm}', reply_markup=await bpm_markup(bpm))
    elif bpm < min_bpm:
        await c.answer('Достигнут минимальный лимит bpm для этого стиля', show_alert=True)
    elif bpm > max_bpm:
        await c.answer('Достигнут максимальный лимит bpm для этого стиля', show_alert=True)


@platinum_router.callback_query(Platinum.lad)
async def choose_ext(c: CallbackQuery,
                     state: FSMContext,
                     user):
    lad = c.data.split(':')[1]
    await state.update_data(lad=lad)
    await state.set_state(Platinum.ext)
    await c.message.edit_text(f'Выберите формат файла', reply_markup=KB_EXT)


@platinum_router.callback_query(Platinum.ext)
async def collect_params(c: CallbackQuery,
                         state: FSMContext,
                         user):
    ext = c.data.split(':')[1]
    chat_id = c.message.chat.id

    await state.update_data(ext=ext)

    data = await state.get_data()

    beat_parameters = {
        'style': data['style'],
        'bpm': data['bpm'],
        'lad': data['lad'],
        'ext': data['ext'],
        'harmonic': parameters.STYLES['platinum'][data['style']][2]['harmonic'],
        'support_bass': parameters.STYLES['platinum'][data['style']][2]['bass']
    }

    await state.clear()

    if user.balance < parameters.BEAT_PRICE['platinum'] and get_user_credits(chat_id).beats < 1:
        return await c.message.edit_text(f'У вас недостаточно средств')

    user_dir = await create_user_dir(str(chat_id))


    try:
        await c.message.edit_text(f'↻ запрос...')

        await beat_req('platinum', chat_id, user_dir, beat_parameters)

        await c.message.edit_text(f'Вы добавлены в генерацию')

    except:

        await asyncio.sleep(2)
        await c.message.edit_text(f'Не удалось получить запрос на генерацию, пожалуйста, попробуйте позже.')
