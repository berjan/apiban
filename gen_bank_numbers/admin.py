from django.contrib import admin
from gen_bank_numbers.models import BankAccount, BankRange

admin.site.register(BankAccount)
# Register your models here.
admin.site.register(BankRange)