from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pyttsx3
import speech_recognition as sr
from datetime import date

# If modifying these scopes, delete the file token.pickle .
# if you run this for the first
# t time it will take you to gmail to choose your account
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def speak(text):
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	rate = engine.getProperty('rate')

	engine.setProperty('rate', rate-20)

	engine.say(text)
	engine.runAndWait()


speak("Welcome to mail service")


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)
		said = ""

	try:
		said = r.recognize_google(audio)
		print(said)

	except:
		speak("Didn't get that")

	return said.lower()


def authenticate_gmail():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
	creds = None

	# The file token.pickle stores the user's
	# access and refresh tokens, and is
	# created automatically when the authorization
	# flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If there are no (valid) credentials available,
	# let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)
	return service


def check_mails(service):

	# fetching emails of today's date
	today = (date.today())

	today_main = today.strftime('%Y/%m/%d')

	# Call the Gmail API
	results = service.users().messages().list(userId='me',
											labelIds=["INBOX", "UNREAD"],
											q="after:{0} and category:Primary".format(today_main)).execute()
	# The above code will get emails from primary
	# inbox which are unread
	messages = results.get('messages', [])

	if not messages:

		# if no new emails
		print('No messages found.')
		speak('No messages found.')
	else:
		m = ""

		# if email found
		speak("{} new emails found".format(len(messages)))

		speak("if you want to read any particular email just type read ")
		speak("and for not reading type leave ")
		for message in messages:

			msg = service.users().messages().get(userId='me',
												id=message['id'], format='metadata').execute()

			for add in msg['payload']['headers']:
				if add['name'] == "From":

					# fetching sender's email name
					a = str(add['value'].split("<")[0])
					print(a)

					speak("email from"+a)
					text = input()

					if text == "read":

						print(msg['snippet'])

						# speak up the mail
						speak(msg['snippet'])

					else:
						speak("email passed")


SERVICE2 = authenticate_gmail()
check_mails(SERVICE2)
