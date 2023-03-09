from django.db import models
from django.forms import ValidationError

# Create your models here.


class Account(models.Model):
    SAVINGS = 'Savings'
    CHECKING = 'Checking'
    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'),
        (CHECKING, 'Checking'),
    ]
    account_number = models.CharField(max_length=200, unique=True)
    balance = models.FloatField()
    customer_name = models.CharField(max_length=200)
    account_type = models.CharField(
        max_length=200, choices=ACCOUNT_TYPE_CHOICES)
    account_creation = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number

    def clean(self):
        super().clean()
        if self.pk is None and self.balance <= 0:
            raise ValidationError(
                "Balance must be greater than 0 for new accounts")

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Balance can not be negative")

        super().save(*args, **kwargs)

    def update_balance(self, transaction):
        if transaction.transaction_type == 'Deposit':
            self.balance += transaction.amount
        elif transaction.transaction_type == 'Withdraw':
            self.balance -= transaction.amount
        self.save()


class Transaction(models.Model):
    DEPOSIT = 'Deposit'
    WITHDRAW = 'Withdraw'
    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
    ]
    transaction_id = models.CharField(max_length=200, unique=True)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=200, choices=TRANSACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.transaction_id

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.transaction_type == 'Withdraw' and self.amount > self.account_number.balance:
            raise ValidationError("Not enough funds in the account")
        super().save(*args, **kwargs)
        self.account_number.update_balance(self)
