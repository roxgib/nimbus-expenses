from datetime import timedelta
from decimal import Decimal

from django.test import TestCase

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

        self.c1 = Client.objects.get(name='Test Client 1')
        self.c2 = Client.objects.get(name='Test Client 2')
        self.e1 = Expense.objects.get(expense="Test Expense 1")
        self.e2 = Expense.objects.get(expense="Test Expense 2")
        self.e3 = Expense.objects.get(expense="Test Expense 3")


    def test_client_str(self):
        self.assertEqual(self.c1.__str__(), "Test Client 1")
        self.assertEqual(self.c2.__str__(), "Test Client 2")

    def test_client_expenses(self):
        self.assertListEqual(list(self.c1.expenses), list())
        self.assertListEqual(list(self.c2.expenses), list(Expense.objects.all()))

    def test_client_total(self):
        self.assertEqual(self.c1.total, 0)
        self.assertEqual(self.c2.total, Decimal('259.21'))

    def test_auth(self):
        auth_code = self.c2.set_auth_code()
        self.assertTrue(self.c2.validate_auth_code(auth_code))
        self.assertFalse(self.c2.validate_auth_code(auth_code))

    def test_auth_wrong_code(self):
        auth_code = self.c2.set_auth_code()
        self.assertFalse(self.c2.validate_auth_code(auth_code + '1'))
        self.assertFalse(self.c2.validate_auth_code(auth_code))

    def test_auth_expired(self):
        auth_code = self.c2.set_auth_code()
        self.c2.auth_expiry -= timedelta(2)
        self.assertFalse(self.c2.validate_auth_code(auth_code))

    def test_expense_str(self):
        self.assertEqual(self.e1.__str__(), 
                        "Test Client 2 (Test Expense 1, $123.45, 1 Jan)")
        self.assertEqual(self.e2.__str__(), 
                        "Test Client 2 (Test Expense 2, $12.30, 1 Jan)")
        self.assertEqual(self.e3.__str__(), 
                        "Test Client 2 (Test Expense 3, $123.46, 1 Jan)")
