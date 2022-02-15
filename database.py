#Challenge MeLi 2022 - Lautaro Stroia

import mysql.connector as sql
from mysql.connector import Error
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

#Database variables
HOST = cfg['mysql']['HOST']
USER = cfg['mysql']['USER']
PW = cfg['mysql']['PW']
DB_NAME = cfg['mysql']['DB_NAME']
DRIVE_TABLE_NAME = cfg['mysql']['DRIVE_TABLE']
LOGS_TABLE_NAME = cfg['mysql']['LOGS_TABLE']

class DataBaseHandler:

	def __init__(self):

		self.database = None
		self.processor = None


	def create_database(self):

		'''Create a connection to a SQL database.
		If the connection is successfull, it creates
		the database if it doesn't exist.
		The connection credentials are obtained from the
		config.ini file
		'''

		try:
			self.database = sql.connect(host = HOST,
										user = USER,
										password = PW,
										database = DB_NAME
							)
			if self.database.is_connected():
				self.processor = self.database.cursor()
				self.processor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DB_NAME))
				self.database.commit()
				print("Database {} connected successfully".format(DB_NAME))

		except Error as e:
			print("Error while connecting to SQL: {}".format(e))
			self.shutdown_database()		


	def create_table(self):

		'''Create the table where all the docs presents in the drive
		will be stored'''

		try:
			self.processor.execute(
				f"CREATE TABLE IF NOT EXISTS {DRIVE_TABLE_NAME}"
				"(id VARCHAR(255) UNIQUE,"
				"file_name VARCHAR(255),"
				"file_type VARCHAR(255),"
				"owner VARCHAR(255),"
				"visible VARCHAR(255),"
				"modified_at VARCHAR(255))"
			)
			self.database.commit()
			print("Table {} created successfully".format(DRIVE_TABLE_NAME))
		except Error as e:
			print("Error while creating drive table: {}".format(e))
			self.shutdown_database()


	def create_logs_table(self):

		'''Create the table where all the docs presents in the drive that
		where once public will be stored'''

		try:
			self.processor.execute(
				f"CREATE TABLE IF NOT EXISTS {LOGS_TABLE_NAME}"
				"(id VARCHAR(255) UNIQUE,"
				"file_name VARCHAR(255),"
				"visible VARCHAR(255))"
			)
			self.database.commit()
			print("Logs table {} created successfully".format(LOGS_TABLE_NAME))
		except Error as e:
			print("Error while creating logs table: {}".format(e))
			self.shutdown_database()


	def save_drive_files(self, data):

		'''It stores in the documents table, all the documents present in the drive
		that have not been saved up to now. If it already exists in the table, the field that
		has different value than the one already saved is replaced'''

		query = "REPLACE INTO {} (id, file_name, file_type, owner, visible, modified_at) VALUES (%s,%s,%s,%s,%s,%s)".format(DRIVE_TABLE_NAME)
		to_insert = (data['id'], data['name'], data['mimeType'], data['owners'][0]['emailAddress'], data['shared'], data['modifiedTime'])
		
		self.processor.execute(query, to_insert)
		self.database.commit()
		print("Saved file with id: {}".format(data['id']))


	def save_drive_logs(self, data):

		'''It stores, in the log table, all the documents present in the drive that where once public'''


		query = "INSERT IGNORE INTO {} (id, file_name, visible) VALUES (%s,%s,%s)".format(LOGS_TABLE_NAME)
		to_insert = (data['id'],data['name'],data['shared'])

		self.processor.execute(query, to_insert)
		self.database.commit()
		print("Saved public file in logs table with id: {}".format(data['id']))


	def change_file_visibility(self, data):

		'''Modifies the "visible" field to indicate that the file is now private'''

		query = "UPDATE {} SET visible = '0' WHERE (id = '{}')".format(DRIVE_TABLE_NAME, data['id'])
		self.processor.execute(query)
		self.database.commit()
		print("Updated visibility of file {} to private".format(data['id']))


	def run(self):

		'''Run the database with their respective tables'''

		self.create_database()
		self.create_table()
		self.create_logs_table()

	def shutdown_database(self):

		'''Close the connection to the database'''

		self.processor.close()
		self.database.close()
		print("Connection closed")



