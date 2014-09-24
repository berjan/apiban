import pdb
import random
import string
import datetime
from django.db import models

# Create your models here.
import time

class BankRange(models.Model):
    bank_range = models.CharField(max_length=4, null=False, blank=False)
    bank = models.CharField(max_length=255, null=False, blank=False)
    iban = models.CharField(max_length=4, null=True, blank=True)
    swift = models.CharField(max_length=10,null=True, blank=True)
    bank_name = models.CharField(max_length=30, null=True, blank=True)


    def __unicode__(self):
        return "%s-%s-%s" % (str(self.bank_range), self.bank, self.swift)
    class Meta:
        unique_together = ("bank_range", "bank")
        ordering = ('bank_range',)

class BankAccount(models.Model):
    number = models.PositiveIntegerField(max_length=9)
    bank = models.CharField(max_length=255, null=True,blank=True)
    iban = models.CharField(max_length=255, null=True, blank=True)
    bic = models.CharField(max_length=244, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    error = models.CharField(max_length=255, null=True, blank=True)
    date_requested = models.DateTimeField()
    date_updated = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_created=True)
    date_now = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.bank_name


    @staticmethod
    def generate_numbers():
        import random
        #numbers in bank account
        ints = "0123456789"

        #ints to be guessed in a range
        guessing_ints = []

        bank_account_numbers_to_check = []

        #create start range bankaccount numbers
        for i in range(1000, 9999, 1):
            guessing_ints.append(i)

        total_guessed = 0
        total_wrong = 0

        #while there are still ints to guess, try to find a suitable number
        while not len(guessing_ints) == 0:
            i = guessing_ints[0]
            random_int = str(i)
            for r in range(0,5,1):
                random_int += random.choice(ints)
            if BankAccount.check_valid(random_int):

                total_guessed += 1

                #remove the guessed range from the list
                guessing_ints.pop(0)

                #add the guessed bank account to the list
                bank_account_numbers_to_check.append(random_int)
            else:
                total_wrong += 1

        #return the correct bank account numbers
        return bank_account_numbers_to_check

    @staticmethod
    def check_valid(number):
        if number:
            # Huidig controlegetal is 9 en totaal = 0
            controleGetal = 9
            totaal = 0
            # Haal een voor een de getallen uit het nummer
            for getal in number:
                # Is het wel een getal?
                if getal in string.digits:
                    # Vermenigvuldig het getal met het controlegetal en tel het op bij het totaal
                    totaal = totaal + int(getal) * controleGetal
                    # Trek 1 af van controlenummer
                    controleGetal = controleGetal - 1
            # Kijk of het nummer geldig is door staartdeling te doen; rest moet 0 zijn
            if divmod(totaal, 11)[1] == 0:
                return True
            else:
                return False

    @staticmethod
    def get_iban_number(number):
        #for ING numbers
        ing = False
        if len(str(number)) == 7:
            number = '00' + number
            ing=True

        if BankAccount.check_valid(number) or ing:
            bank = None
            try:
                bank = BankRange.objects.get(bank_range=str(number)[:2])
            except:
                pass

            try:
                bank = BankRange.objects.get(bank_range=str(number)[:3])
            except:
                pass

            try:
                bank = BankRange.objects.get(bank_range=str(number)[:4])
            except:
                pass

            if not bank:
                return False
            else:
                #bank_account = BankAccount.objects.filter(bank=bank.bank, iban__icontains=bank.iban)[0]
                raw_number =  'NL01' + bank.iban + '0' + str(number)
                #pdb.set_trace()
                check_sum = BankAccount.checksum_iban(raw_number)
                if len(str(check_sum)) == 1:
                    check_sum = '0' + str(check_sum)
                new_number = raw_number[:2] + str(check_sum) + raw_number[4:]
                return new_number
    @staticmethod
    def mod97(digit_string):
    #"""Modulo 97 for huge numbers given as digit strings.
    #
    #This function is a prototype for a JavaScript implementation.
    #In Python this can be done much easier: long(digit_string) % 97.
    #"""
        m = 0
        for d in digit_string:
            m = (m * 10 + int(d)) % 97
        return m

    @staticmethod
    def checksum_iban(iban):

        code     = iban[:2]
        checksum = iban[2:4]
        bban     = iban[4:]

        # Assemble digit string
        digits = ""
        for ch in bban.upper():
            if ch.isdigit():
                digits += ch
            else:
                digits += str(ord(ch) - ord("A") + 10)
        for ch in code:
            digits += str(ord(ch) - ord("A") + 10)

        digits += "00"

        # Calculate checksum
        checksum = 98 - BankAccount.mod97(digits)
        return checksum


    @staticmethod
    def get_bank_json():
        bank_numbers_to_check = BankAccount.generate_numbers()
        int_bank_number = []
        for i in range(0, len(bank_numbers_to_check), 1):
            int_bank_number.append(i)



        for i in range(0, 4000, 1):
            choice = random.choice(int_bank_number)


            int_random = []
            for i in range(1, 4, 1):
                int_random.append(i)
            sleep_sec = random.choice(int_random)
            time.sleep(sleep_sec)
            import urllib2
            import json

            response = urllib2.urlopen('http://www.openiban.nl/?rekeningnummer=%s&output=json' % bank_numbers_to_check[choice])
            data = json.load(response)
            bank = data['bank']
            bank_name = data['bankofficialname']
            iban = data['iban']
            bic = data['bic']
            try:
                error = data['error']
            except:
                error = ""
            try:
                BankAccount.objects.get(number=bank_numbers_to_check[choice])
            except:

                b = BankAccount()
                b.bank = bank
                b.bank_name = bank_name
                b.bic = bic
                b.iban = iban
                b.error = error
                b.number = int(bank_numbers_to_check[choice])
                b.date_created = datetime.datetime.now()
                b.date_requested = datetime.datetime.now()
                b.save()

                print "rekening %s heeft bank %s" % (bank_numbers_to_check[choice], bank)

    @staticmethod
    def get_range_account_numbers():
        bank_accounts = BankAccount.objects.all()
        dict_bank_account = {}
        for a in bank_accounts:
            dict_bank_account[a.number] = a.bank

        first_nine = "123456789"

        bank_counter = {}
        for number, bank in dict_bank_account.iteritems():
            for first_range in range(10, 100):


                if str(number)[:1] == str(first_range):

                    if not bank in bank_counter:
                        bank_counter[bank] = {}

                        if not first_range in bank_counter[bank]:
                            bank_counter[bank][first_range] = 1
                    else:
                        if not first_range in bank_counter[bank]:
                                bank_counter[bank][first_range] = 1
                        else:
                            bank_counter[bank][first_range] += 1

                if str(number)[:2] == str(first_range):

                    if not bank in bank_counter:
                        bank_counter[bank] = {}

                        if not first_range in bank_counter[bank]:
                            bank_counter[bank][first_range] = 1
                    else:
                        if not first_range in bank_counter[bank]:
                                bank_counter[bank][first_range] = 1
                        else:
                            bank_counter[bank][first_range] += 1

        for bank, value in bank_counter.iteritems():
            #pdb.set_trace()
            if not bank == "":
                for v in value:
                    try:
                        b, _ = BankRange.objects.get_or_create(bank_range=v, bank=bank)
                    except:
                        #is not unique
                        pass



        #check for doubles
        test_dict = {}
        double_dict = {}
        for bank, value in bank_counter.iteritems():
            if not bank == "":
                for v in value:
                    if not v in test_dict:
                        test_dict[v] = bank
                    else:
                        if not test_dict[v] == bank:
                            if not v in double_dict:
                                double_dict[v] = {bank:test_dict[v]}

        find_unique_numbers_bank = {}
        for d in double_dict:

            for number, bank in dict_bank_account.iteritems():
                for r in range(d *10, d *10 + 10):

                    if str(number)[:3] == str(r):

                        if not bank in find_unique_numbers_bank:
                            find_unique_numbers_bank[bank] = {}

                            if not r in find_unique_numbers_bank[bank]:
                                find_unique_numbers_bank[bank][r] = 1
                        else:
                            if not r in find_unique_numbers_bank[bank]:
                                    find_unique_numbers_bank[bank][r] = 1
                            else:
                                find_unique_numbers_bank[bank][r] += 1
        for a in double_dict:
            BankRange.objects.filter(bank_range=a).delete()

        for bank, value in find_unique_numbers_bank.iteritems():
            #pdb.set_trace()
            if not bank == "":
                for v in value:

                    try:
                        b, _ = BankRange.objects.get_or_create(bank_range=v, bank=bank)
                    except:
                        #is not unique
                        pass



        #check for doubles
        test_dict2 = {}
        double_dict2 = {}
        for bank, value in find_unique_numbers_bank.iteritems():
            if not bank == "":
                for v in value:
                    if not v in test_dict2:
                        test_dict2[v] = bank
                    else:
                        if not test_dict2[v] == bank:
                            if not v in double_dict:
                                double_dict2[v] = {bank:test_dict2[v]}


        find_unique_numbers_bank2 = {}
        for d in double_dict2:

            for number, bank in dict_bank_account.iteritems():
                for r in range(d *10, d *10 + 10):

                    if str(number)[:4] == str(r):

                        if not bank in find_unique_numbers_bank2:
                            find_unique_numbers_bank2[bank] = {}

                            if not r in find_unique_numbers_bank2[bank]:
                                find_unique_numbers_bank2[bank][r] = 1
                        else:
                            if not r in find_unique_numbers_bank2[bank]:
                                    find_unique_numbers_bank2[bank][r] = 1
                            else:
                                find_unique_numbers_bank2[bank][r] += 1

        for a in double_dict2:
            BankRange.objects.filter(bank_range=a).delete()

        for bank, value in find_unique_numbers_bank2.iteritems():
            #pdb.set_trace()
            if not bank == "":
                for v in value:

                    try:
                        b, _ = BankRange.objects.get_or_create(bank_range=v, bank=bank)
                    except:
                        #is not unique
                        pass
        #check for doubles
        test_dict3 = {}
        double_dict3 = {}
        for bank, value in find_unique_numbers_bank2.iteritems():
            if not bank == "":
                for v in value:
                    if not v in test_dict3:
                        test_dict3[v] = bank
                    else:
                        if not test_dict3[v] == bank:
                            if not v in double_dict:
                                double_dict3[v] = {bank:test_dict3[v]}



        BankAccount.get_ibans_codes()

        BankRange.objects.create(bank_range='00', iban='INGB', bank='ING',swift='INGBNL2A', bank_name='ING Bank N.V.')
    @staticmethod
    def get_ibans_codes():
        abn_numbers = BankAccount.objects.values('number', 'iban').all()

        for r in BankRange.objects.all():
            bank_obj = BankAccount.objects.values('iban', 'bank_name', 'bic').filter(number__startswith=r.bank_range)[0]
            iban = bank_obj['iban'][4:8]
            r.iban = iban
            r.bank_name = bank_obj['bank_name']
            r.swift = bank_obj['bic']
            r.save()











