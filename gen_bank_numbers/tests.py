import pdb
import random
from django.test import TestCase

# Create your tests here.
import time
from gen_bank_numbers.models import BankAccount


class BankAccountTestCase(TestCase):
    def setUp(self):
        pass



    def test_valid_bank_account(self):
        self.assertEqual(BankAccount.check_valid("394003489"), True)

    def test_bank_account_numbers(self):
        pass
        self.assertEqual(len(BankAccount.generate_numbers()), 8999)

    def test_range_banks(self):
        BankAccount.get_range_account_numbers()



















