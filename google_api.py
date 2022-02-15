#Challenge MeLi 2022 - Lautaro Stroia

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import os.path
import pickle
import base64
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

USER_EMAIL = cfg['google']['USER']

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']

class GoogleAPIHandler:

	@classmethod
	def get_service(cls, platform, api_version):

		'''Returns a GDrive API Service to handle drive files if api_version = "v3"
		and platform = "drive",	else returns a gmail service to send emails'''

		credentials = None

		#token.pickle stores access tokens
		#it is auto-created after the first run

		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				credentials = pickle.load(token)

		#No credentials? user must log in

		if not credentials or not credentials.valid:
			if credentials and credentials.expired and credentials.refresh_token:
				credentials.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
				credentials = flow.run_local_server(port = 0)

			#store credentials
			with open('token.pickle', 'wb') as token:
				pickle.dump(credentials, token)

		#return gdrive api service

		return build(platform, api_version, credentials = credentials)


	@classmethod
	def get_drive_files(cls):

		'''Returns the files present in a GDrive account'''
		
		service = cls.get_service('drive','v3')
		results = service.files().list(
			pageSize = 1000,
			fields = "nextPageToken, files(id, name, mimeType, owners, shared, size, parents, modifiedTime, permissions)").execute()
		files = results.get('files', [])
		return files


	@classmethod
	def modify_permissions(cls, fileId, permissionId):

		'''Changes the permissions of the file "fileId"'''
		service = cls.get_service('drive', 'v3')
		service.permissions().delete(fileId = fileId,permissionId = permissionId).execute()


	@classmethod
	def send_email(cls, receiver, subject, text):

		'''Create a message for an email and send it.
		Args:
			*receiver: email address of the receiber
			*subject: subject of the email
			*text: text of the email
			*The sender email address is stored in config.ini'''

		gmail_service = cls.get_service('gmail','v1')
		msg = MIMEText(text)
		msg['to'] = receiver
		msg['from'] = USER_EMAIL
		msg['subject'] = subject

		to_send = {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}
		gmail_service.users().messages().send(userId = USER_EMAIL, body = to_send).execute()
		print("Email successfully sent to {}".format(receiver))


