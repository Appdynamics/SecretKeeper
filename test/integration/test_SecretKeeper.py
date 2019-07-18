import os
import unittest
from secretkeeper import SecretKeeper as sk

class TestSecret(unittest.TestCase):
    def setUp(self):
        self.client = sk.SecretKeeper()
        self.test_secret = 'test_secret_9'

    def test_1_create_secret(self):
        p = {
            'name': self.test_secret,
            'desc': 'integration_test_secret',
            'secret': '1234ABCDEFG!#$%1231',
            'key_id': os.environ.get('test_kms_id')
        }
        r = self.client.create_secret(**p)
        self.assertIsNotNone(r)

    def test_2_get_secret(self):
        r = self.client.get_secret(self.test_secret)
        print(r)
        self.assertIsNotNone(r)

    def test_3_delete_secret(self):
        r = self.client.delete_secret(secret_id=self.test_secret)
        self.assertIsNotNone(r)

if __name__ == '__main__':
    unittest.main()