#!/usr/bin/env python3
import requests
import json
import time
import datetime
import os

from pathlib import Path
from urllib import request
from urllib.error import HTTPError
from json import loads

d = datetime.datetime.utcnow()
d = d + datetime.timedelta(days=-1)
d = d.isoformat("T") + "Z"

WEBHOOK_URL = 'YOUR_WEBHOOK_URL'
PATH = 'YOUR_PATH' #Path where you stock clip id for doesnt spam discord

API_ENDPOINT = 'https://api.twitch.tv/helix/clips?broadcaster_id=54543758&started_at={}'.format(d)

#Create app https://dev.twitch.tv/console/apps
Client_ID = 'CLIENT_ID'
#Get twitch token https://id.twitch.tv/oauth2/authorize?client_id=CLIENT_APP_ID&redirect_uri=URI_APP&response_type=token
TOKEN = 'Bearer YOUR_TOKEN'

#data to be sent to api
head = {
"Authorization":  TOKEN,
'Client-ID' : Client_ID,
'Accept': 'application/vnd.twitchtv.v5+json'
}
#api call here
r = requests.get(url = API_ENDPOINT, headers = head)

for clip in loads(r.text)['data']:
    # La payload
	payload = {
		'username':"New Clip!",
		'content': "A new clip has been created {} By {}".format(clip['url'],clip["creator_name"]),
		'avatar_url':"https://i.imgur.com/VGpObLh.png",
	}

	# Les paramètres d'en-tête de la requête
	headers = {
		'Content-Type': 'application/json',
		'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
	}
	
	# Enfin on construit notre requête
	req = request.Request(url=WEBHOOK_URL,
				  data=json.dumps(payload).encode('utf-8'),
				  headers=headers,
				  method='POST')

	if os.path.exists('{}/clips/{}'.format(PATH,clip['id']))==True:
		print('exist')
	else:
		response = request.urlopen(req)
		open('{}/clips/{}'.format(PATH,clip['id']), "x")
