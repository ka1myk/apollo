import requests


def send_to_telegram(message):
    token = "5704394405:AAEQcpb0t8GJ69imJXVbn7d2fdAbc0hScmE"
    userID = "203161038"

    # Create url
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Create json link with message
    data = {'chat_id': userID, 'text': message}

    # POST the message
    requests.post(url, data)
