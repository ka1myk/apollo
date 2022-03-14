message = ":white_check_mark: VPS and passivbot rebooted"

def send_to_telegram(message):
    import telegram

    telegram_http_api = "1919249173:AAHLjSdJUUtnieEjYPlzPdfxf4gqldSg35I"
    telegram_user_id = "203161038"

    bot_binance = telegram.Bot(token=telegram_http_api)
    bot_binance.send_message(chat_id=telegram_user_id, text=message, parse_mode='HTML')

send_to_telegram(message)
