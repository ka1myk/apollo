message = ":white_check_mark: VPS and passivbot rebooted"

def telegram_bot_sendtext(bot_message):
   
    import requests
   
    bot_token = "1919249173:AAHLjSdJUUtnieEjYPlzPdfxf4gqldSg35I"
    bot_chatID = "203161038"
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

telegram_bot_sendtext(message)
