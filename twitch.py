import requests

# Twitch API credentials
twitch_client_id = ''
twitch_client_secret = ''

# Check streamer's status
def check_stream_status(twitch_username):
    url = f'https://api.twitch.tv/helix/streams?user_login={twitch_username}'
    headers = {
        'Client-ID': twitch_client_id,
        'Authorization': f'Bearer {get_access_token()}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        return True  # Streamer is live
    return False  # Streamer is not live

# Get Twitch access token
def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': twitch_client_id,
        'client_secret': twitch_client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    data = response.json()
    return data['access_token']
