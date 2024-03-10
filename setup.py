import json

print('Thanks for using DiscordAutoSender!')
print('Repository: https://github.com/gallen881/DiscordAutoSender')

config = {}

config['bot_token'] = input('Enter your bot token:?')
config['user_token'] = input('Enter your user token:?')
config['message_prefix'] = '**AutoSend: **'

with open('config.json', 'w') as f:
    json.dump(config, f, indent=4)
with open('messages.json', 'w') as f:
    json.dump([], f, indent=4)