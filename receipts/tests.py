# from django.test import TestCase
from unittest import TestCase
from receipts.models import Client
from receipts.auth import validate_email_authentication, send_auth_email


class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(
            name = "Test Client 1",
            email = "test@example.com",
            username = "Test 2",
            )

        Client.objects.create(
            name = "Test Client 2",
            email = "test2@example.com",
            username = "Test 2",
            )

    def test_properties(self):
        client1 = Client.objects.get(name='Test Client 1')
        client2 = Client.objects.get(name='Test Client 2')

        self.assertEqual(client1.__str__(), "Test Client 1")
        self.assertEqual(client2.__str__(), "Test Client 2")

        self.assertEqual(client1.expenses, None)
        self.assertEqual(client2.expenses, None)

        self.assertEqual(client1.total, 0)
        self.assertEqual(client2.total, 0)





# auth_code = send_auth_email(client)

# assert validate_email_authentication(client, auth_code) 