# wowwait_parser.py
import requests
from bs4 import BeautifulSoup
import os
import time

import telegram

filepath = 'log/latest.txt'

# call the bot (need to put your own token to send a message)
bot = telegram.Bot(token='982181935:AAG9ScQJkt5O2lt1WZnm7Q9VNEi4nwj_wSc')		# fill the token argument with your own token

chat_id = bot.getUpdates()[-1].message.chat.id


# the location of file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


while True:
	req = requests.get('http://wowwait.com')
	req.encoding = 'utf-8'	# prepare against that they do not send an encoding information.

	html = req.text
	soup = BeautifulSoup(html, 'html.parser')

	# parsing information
	wait_ppls = str(soup.select('td:nth-child(4)')[0])[4:-5]
	wait_ppls_int = int(str(soup.select('td:nth-child(4)')[0])[4:-7])
	wait_time = str(soup.select('td:nth-child(5)')[0])[10:-6]
	wait_time_int = int(str(soup.select('td:nth-child(5)')[0])[10:-8])
	expected_conntime = str(soup.select('td:nth-child(5)')[0])[4:-11]
	latest = str(soup.select('td:nth-child(6)')[0])[4:-12]


	if not os.path.exists(BASE_DIR):
		os.makedirs(BASE_DIR)

	with open(os.path.join(BASE_DIR, filepath), 'r+') as f_read:
		before = f_read.readline()
		f_read.close()

		if before != latest:
			new_msg = '[WoW Wait Bot]\n현재 로크홀라 서버의 대기열은 [' + wait_ppls + '] 이며, 대기 시간은 [' + wait_time[:5] + '] 입니다.\n현재 접속할 시, 예상 접속 가능 시각은 [' + expected_conntime + '] 입니다. \n - 정보 업데이트 시각 : ' + latest
			bot.sendMessage(chat_id=chat_id, text=new_msg)

			with open(os.path.join(BASE_DIR, filepath), 'w+') as f_write:
				f_write.write(latest)
				f_write.close()

			if wait_time_int >= 30 and wait_time_int < 45:
				new_msg = '[WoW Wait Bot]\n현재 로크홀라 서버 대기 시간이 [' + wait_time[:5] + '] 을 돌파했습니다.\n - 정보 업데이트 시각 : ' + latest

			if wait_time_int >= 45 and wait_time_int < 60:
				new_msg = '[WoW Wait Bot]\n현재 로크홀라 서버 대기 시간이 [' + wait_time[:5] + '] 을 돌파했습니다.\n - 정보 업데이트 시각 : ' + latest				

			if wait_time_int >= 60 and wait_time_int < 120:
				new_msg = '[WoW Wait Bot]\n현재 로크홀라 서버 대기 시간이 [' + wait_time[:5] + '] 을 돌파했습니다.\n - 정보 업데이트 시각 : ' + latest

			if wait_time_int >= 120:
				new_msg = '[WoW Wait Bot]\n현재 로크홀라 서버 대기 시간이 [' + wait_time[:5] + '] 을 돌파했습니다.\n지금 접속하지 않으면 정상적인 게임 접속이 힘들어집니다.\n - 정보 업데이트 시각 : ' + latest