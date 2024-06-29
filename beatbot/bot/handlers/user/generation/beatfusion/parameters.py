import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.middlewares import UserDataMiddleware
from bot.database.methods.get import get_user_credits
from bot.states.generation import Beatfusion
from bot.keyboards.inline.beats.beatfusion import *
from bot.web.requests.Service import beat_req
from bot.misc import create_user_dir, parameters

beatfusion_router = Router()

beatfusion_router.callback_query.outer_middleware(UserDataMiddleware())


@beatfusion_router.callback_query(F.data == 'generation:beatfusion')
async def choose_style(c: CallbackQuery,
                       state: FSMContext,
                       user):
    await state.set_state(Beatfusion.style)
    await c.message.edit_text(f'Выберите стиль', reply_markup=await styles_markup())


@beatfusion_router.callback_query(Beatfusion.style)
async def choose_main_instrument(c: CallbackQuery,
                                 state: FSMContext,
                                 user):
    c_data = c.data.split(':')
    await state.update_data(style=c_data[0],
                            min_bpm=c_data[1],
                            max_bpm=c_data[2])
    await state.set_state(Beatfusion.main_instrument)
    await c.message.edit_text(f'Выберите инструмент', reply_markup=await main_instruments_markup())


@beatfusion_router.callback_query(Beatfusion.main_instrument)
async def choose_bpm(c: CallbackQuery,
                     state: FSMContext,
                     user):
    instrument = c_data = c.data.split(':')[1]
    await state.update_data(main_instrument=instrument)
    await state.set_state(Beatfusion.bpm)
    await c.message.edit_text(f'Выберите bpm', reply_markup=await bpm_markup(130))


@beatfusion_router.callback_query(Beatfusion.bpm)
async def choose_lad(c: CallbackQuery,
                     state: FSMContext,
                     user):
    data = await state.get_data()

    c_data = c.data.split(':')

    if c_data[0] == 'submit':
        await state.update_data(bpm=c_data[1])
        await state.set_state(Beatfusion.lad)
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


@beatfusion_router.callback_query(Beatfusion.lad)
async def choose_tonality(c: CallbackQuery,
                          state: FSMContext,
                          user):
    lad = c.data.split(':')[1]
    await state.update_data(lad=lad)
    await state.set_state(Beatfusion.tonality)
    await c.message.edit_text(f'Выберите тональность', reply_markup=KB_TONALITIES)


@beatfusion_router.callback_query(Beatfusion.tonality)
async def choose_ext(c: CallbackQuery,
                     state: FSMContext,
                     user):
    tonality = c.data.split(':')[1]
    await state.update_data(tonality=tonality)
    await state.set_state(Beatfusion.ext)
    await c.message.edit_text(f'Выберите формат файла', reply_markup=KB_EXT)


@beatfusion_router.callback_query(Beatfusion.ext)
async def collect_params(c: CallbackQuery,
                         state: FSMContext,
                         user):
    ext = c.data.split(':')[1]
    chat_id = c.message.chat.id

    await state.update_data(ext=ext)

    data = await state.get_data()

    beat_parameters = {
        'style': data['style'],
        'instrument': data['instrument'],
        'bpm': data['bpm'],
        'lad': data['lad'],
        'tonality': data['tonality'],
        'ext': data['ext'],

    }

    await state.clear()

    if user.balance < parameters.BEAT_PRICE['beatfusion'] and get_user_credits(chat_id).beats < 1:
        return await c.message.edit_text(f'У вас недостаточно средств')

    user_dir = await create_user_dir(str(chat_id))

    try:
        await c.message.edit_text(f'↻ запрос...')

        await beat_req('beatfusion', chat_id, user_dir, beat_parameters)

        await c.message.edit_text(f'Вы добавлены в генерацию')

    except:

        await asyncio.sleep(2)
        await c.message.edit_text(f'Не удалось получить запрос на генерацию, пожалуйста, попробуйте позже.')
