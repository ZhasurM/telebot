#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from config import TOKEN
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# GENDER, PHOTO, LOCATION, BIO = range(4)
(
    NAME, 
    TELEPHONE, 
    DATE, 
    GUESTS, 
    FORMAT, 
    DURATION, 
    LOCATION, 
    KITCHEN, 
    BUDGET,
    POZHELANIYA,
    COMPLITE
) = range(11)

main_keyboard = [
    ["Просмотреть меню"],
    ["Сделать заказ"],
    ["Связаться с нами", "Оставить отзыв"],
]
main_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)


keyboard_for_order = [
    ["Age", "Favourite colour"],
    ["Number of siblings", "Something else..."],
    ["Done"],
]
order_markup = ReplyKeyboardMarkup(keyboard_for_order, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Для того что бы максимально точно ответить на вопрос <<Сколько стоит банкет или фуршет?>>"""
    await update.message.reply_text(
        "Здравствуйте!",
        reply_markup=main_markup,
    )


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and asks the user their name."""
    await update.message.reply_text(
        "Как Вас зовут?",
        reply_markup=ReplyKeyboardMarkup(
            [[update.message.from_user.first_name]], 
            resize_keyboard=True,
            one_time_keyboard=True
        ),
    )
    return NAME




async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the name and asks tel."""
    text = update.message.text
    context.user_data["name"] = text
    await update.message.reply_text(
        "Введите, пожалуйста, номер телефона для связи",
        reply_markup=ReplyKeyboardRemove(),
    )

    return TELEPHONE


async def telephone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the telephone and asks for a date."""
    text = update.message.text
    context.user_data["telephone"] = text
    await update.message.reply_text(
        "Введите дату проведения мероприятия"
        "\n*например, 25 сентябрь 2022",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DATE


async def ivent_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the date and asks for a guests."""
    text = update.message.text
    context.user_data["date"] = text
    await update.message.reply_text(
        "Предпологаемое количество гостей",
        reply_markup=ReplyKeyboardRemove(),
    )

    return GUESTS


async def guests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the guests and ask for a ivent format"""
    text = update.message.text
    context.user_data["guests"] = text
    await update.message.reply_text(
        "Формат мероприятия (нужное подчеркнуть,"
        " а лучше подробно описать: банкет, фуршет,"
        " выездное обслуживание, только доставка,"
        " свадьба, юбилей, корпоратив, День рождения и т.д.)"
    )
    return FORMAT


async def ivent_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the guests and asks for a format."""
    text = update.message.text
    context.user_data["format"] = text
    await update.message.reply_text(
        "Продолжительность праздника в часах. Чтобы"
        " понимать, какое количество блюд мы можем предложить."
        "\n *нужно ввести число",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DURATION


async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the format and asks for a duration."""
    text = update.message.text
    context.user_data["duration"] = text
    await update.message.reply_text(
        "Локация мероприятия или адрес доставки блюд.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the duration and asks for a location."""
    text = update.message.text
    context.user_data["location"] = text
    await update.message.reply_text(
        "Наличие кухни на площадке, если нет — мы привезём с собой.",
        reply_markup=ReplyKeyboardMarkup(
            [["Есть", "Нет"]], 
            resize_keyboard=True, 
            one_time_keyboard=True
        ),
    )

    return KITCHEN


async def kitchen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for a kitchen."""
    text = update.message.text
    context.user_data["kitchen"] = text
    await update.message.reply_text(
        "Примерный бюджет на персону."
        "\n*в сумах",
        reply_markup=ReplyKeyboardRemove(),
    )

    return BUDGET


async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the kitchen and asks for a budget."""
    text = update.message.text
    context.user_data["budget"] = text
    await update.message.reply_text(
        "Ваши пожелания: Ваши пожелания: возможно, кто-то из гостей вегетарианец, или не ест определенные продукты, пишите все, что нужно знать о вас и ваших гостях."
    )

    return POZHELANIYA


async def pozhelaniya(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the budget and asks for a pozhelaniya."""
    ans = update.message.text
    context.user_data["pozhelaniya"] = ans
    text = context.user_data
    dt = """
    <strong>Ваша заявка сохранена, мы свяжемся с вами в ближайшее время.</strong>
    -----------------------------------------------------
    <b>Детали заказа</b>
    Имя: {}
    Номер: {}
    Дата проведения: {}
    Количество предпологаемых гослей: {}
    Формат мероприятия: {}
    Продолжительность: {} часов
    Место проведения: {}
    Наличие кухни: {}
    Примерный бюджет на персону: {} сумов
    Пожелания: {}
    """.format(
        text["name"], 
        text["telephone"],
        text["date"],
        text["guests"],
        text["format"],
        text["duration"],
        text["location"],
        text["kitchen"],
        text["budget"],
        text["pozhelaniya"]
        )


    await update.message.reply_text(dt, parse_mode='html', reply_markup=main_markup)

    return ConversationHandler.END


async def complit_hand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the pozhelaniay and complite handler"""
    text = context.user_data
    await update.message.reply_text(
        reply_markup=main_markup,
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5502944192:AAHUEkhVTJZE5K0WyhnUvKK1Q_IpKp75QY0").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Сделать заказ$"), order)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            TELEPHONE: [MessageHandler(filters.TEXT, telephone)],
            DATE: [MessageHandler(filters.TEXT, ivent_date)],
            GUESTS: [MessageHandler(filters.TEXT, guests)],
            FORMAT: [MessageHandler(filters.TEXT, ivent_format)],
            DURATION: [MessageHandler(filters.TEXT, duration)],
            LOCATION: [MessageHandler(filters.TEXT, location)],
            KITCHEN: [MessageHandler(filters.TEXT, kitchen)],
            BUDGET: [MessageHandler(filters.TEXT, budget)],
            POZHELANIYA: [MessageHandler(filters.TEXT, pozhelaniya)],
            COMPLITE: [MessageHandler(filters.TEXT, complit_hand)]
        },
        fallbacks=[CommandHandler("cancel", complit_hand)],
    )

    application.add_handler(CommandHandler("start", start))

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()










