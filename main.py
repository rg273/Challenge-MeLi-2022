#Challenge MeLi 2022 - Lautaro Stroia

from database import *
from google_api import *


def main():

	#Database

	try:
		db = DataBaseHandler()
		db.run()
	except Exception:
		print("Error with database")
		return

	#Google API service

	gapi_handler = GoogleAPIHandler()

	try:
		files = gapi_handler.get_drive_files()
	except Exception as e:
		print("Error with GDrive API Service: {}".format(e))
		return

	if len(files) == 0 or not files:
		print("Files not found")
		return

	for file in files:
		db.save_drive_files(file)		
		if file['shared'] is True:
			db.save_drive_logs(file)
			file['shared'] = False
			owner_perm_id = file['owners'][0]['permissionId']

			for user in file['permissions']:
				if user['id'] != owner_perm_id:
					gapi_handler.modify_permissions(file['id'], user['id'])
					db.change_file_visibility(file)

			#send email
			receiver = file['owners'][0]['emailAddress']
			subject = 'Google Drive - a file has been modified'
			text = "The visibility of your file {} has been modified for security reasons. Sorry for the incovenience.".format(file['name'])
			gapi_handler.send_email(receiver, subject, text)


	db.shutdown_database()
	return None


if __name__ == '__main__':
    main()