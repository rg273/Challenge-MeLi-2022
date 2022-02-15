#Challenge MeLi 2022 - Lautaro Stroia

import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock, patch
from database import *
from google_api import *
import main



class MeliChallengeTest(TestCase):

	@patch.object(GoogleAPIHandler, 'get_service')
	@patch.object(GoogleAPIHandler, 'get_drive_files')	
	@patch.object(GoogleAPIHandler, 'modify_permissions')
	def test2(self, mock_perm, mock_files, mock_svc):

		google_api = GoogleAPIHandler()
		test_file = {'id': '1tBINCkA9aWfKLO4zba_JIXG26JVkRzGJ',
					   'name': 'testing.tar.gz',
					   'mimeType': 'application/gzip',
					   'parents': ['0AMe2lSXEcr-uUk9PVA'],
					   'modifiedTime': '2022-02-15T17:33:25.040Z',
					   'owners': [{'kind': 'drive#user',
					   			   'displayName': 'Dev test',
					   			   'photoLink': 'https://lh3.googleusercontent.com/a/default-user=s64',
					   			   'me': True,
					   			   'permissionId': '07275',
					   			   'emailAddress': 'dev.testing.stroia@gmail.com'}],
					   	'shared': True,
					   	'permissions': [{'kind': 'drive#permission',
					   					 'id': 'anyoneWithLink',
					   					 'type': 'anyone',
					   					 'role': 'reader',
					   					 'allowFileDiscovery': False},
					   					{'kind': 'drive#permission',
					   					 'id': '07275',
					   					 'type': 'user',
					   					 'emailAddress': 'dev.testing.stroia@gmail.com',
					   					 'role': 'owner',
					   					 'displayName': 'Dev test',
					   					 'photoLink': 'https://lh3.googleusercontent.com/a/default-user=s64',
					   					 'deleted': False,
					   					 'pendingOwner': False}],
					   					 'size': '93680155'
					}

		test_file_modified = {'id': '1tBINCkA9aWfKLO4zba_JIXG26JVkRzGJ',
					   'name': 'testing.tar.gz',
					   'mimeType': 'application/gzip',
					   'parents': ['0AMe2lSXEcr-uUk9PVA'],
					   'modifiedTime': '2022-02-15T17:33:25.040Z',
					   'owners': [{'kind': 'drive#user',
					   			   'displayName': 'Dev test',
					   			   'photoLink': 'https://lh3.googleusercontent.com/a/default-user=s64',
					   			   'me': True,
					   			   'permissionId': '07275',
					   			   'emailAddress': 'dev.testing.stroia@gmail.com'}],
					   	'shared': False,
					   	'permissions': [{'kind': 'drive#permission',
					   					 'id': '07275',
					   					 'type': 'user',
					   					 'emailAddress': 'dev.testing.stroia@gmail.com',
					   					 'role': 'owner',
					   					 'displayName': 'Dev test',
					   					 'photoLink': 'https://lh3.googleusercontent.com/a/default-user=s64',
					   					 'deleted': False,
					   					 'pendingOwner': False}],
					   					 'size': '93680155'
					}
		mock_svc.build.return_value = None
		mock_perm.permissions.delete.execute.return_value = None
		mock_perm.return_value = None

		mock_files.return_value = test_file

		files = google_api.get_drive_files()

		self.assertEqual(files, test_file)
		google_api.modify_permissions('1tBINCkA9aWfKLO4zba_JIXG26JVkRzGJ', 'anyoneWithLink')
		
		mock_files.return_value = test_file_modified

		files_modified = google_api.get_drive_files()

		self.assertEqual(files_modified, test_file_modified)


if __name__ == '__main__':
	unittest.main()