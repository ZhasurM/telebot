main_keyboard = [
    ["Просмотреть меню"],
    ["Сделать заказ"],
    ["Связаться с нами", "Оставить отзыв"],
]
main_markup = ReplyKeyboardMarkup(main_keyboard)


keyboard_for_order = [
    ["Age", "Favourite colour"],
    ["Number of siblings", "Something else..."],
    ["Done"],
]
order_markup = ReplyKeyboardMarkup(keyboard_for_order, one_time_keyboard=True)