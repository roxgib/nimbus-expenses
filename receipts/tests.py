from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.db import models
from receipts.models import Client, Expense


class MainTestCase(TestCase):
    def setUp(self):
        Client.objects.create(
            name = "Test Client 1",
            email = "test1@example.com",
            username = "Test 1",
            )

        Client.objects.create(
            name = "Test Client 2",
            email = "test2@example.com",
            username = "Test 2",
            )

        Expense.objects.create(
            expense = "Test Expense 1",
            amount = '123.45',
            date = "2022-01-01 00:00",
            gst = True,
            image = "./expenses/test1.png",
            date_added = "2022-02-01 00:00",
            client = Client.objects.get(name="Test Client 2"),
        )

        Expense.objects.create(
            expense = "Test Expense 2",
            amount = '12.3',
            date = "2022-01-01 00:00",
            gst = True,
            image = "./expenses/test2.png",
            date_added = "2022-02-01 00:00",
            client = Client.objects.get(name="Test Client 2"),
        )

        Expense.objects.create(
            expense = "Test Expense 3",
            amount = '123.45678',
            date = "2022-01-01 00:00",
            gst = False,
            image = "./expenses/test3.png",
            date_added = "2022-02-01 00:00",
            client = Client.objects.get(name="Test Client 2"),
        )

    def test_auth(self):
        client = Client.objects.get(name="Test Client 2")
        auth_code = client.set_auth_code()
        self.assertTrue(client.validate_auth_code(auth_code))
        self.assertFalse(client.validate_auth_code(auth_code))

    def test_auth_wrong_code(self):
        client = Client.objects.get(name="Test Client 2")
        auth_code = client.set_auth_code()
        self.assertFalse(client.validate_auth_code(auth_code + '1'))
        self.assertFalse(client.validate_auth_code(auth_code))

    def test_auth_expired(self):
        client = Client.objects.get(name="Test Client 2")
        auth_code = client.set_auth_code()
        client.auth_expiry -= timedelta(2)
        self.assertFalse(client.validate_auth_code(auth_code))

    def test_client(self):
        client1 = Client.objects.get(name='Test Client 1')
        client2 = Client.objects.get(name='Test Client 2')

        self.assertEqual(client1.__str__(), "Test Client 1")
        self.assertEqual(client2.__str__(), "Test Client 2")

        self.assertEqual(list(client1.expenses), list())
        self.assertEqual(list(client2.expenses), list(Expense.objects.all()))

        self.assertEqual(client1.total, 0)
        self.assertEqual(client2.total, Decimal('259.21'))