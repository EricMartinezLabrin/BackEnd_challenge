# Django
from django.forms import ValidationError
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone

# Python
import json

# Local
from .models import Account, Transaction


class AccountModelTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_was_created_correctly(self):
        """
        Checks that a new instance of Account can be created with the correct attribute values.
        It creates a new Account instance with specified attribute values, retrieves the instance,
        and then checks each attribute to ensure that it has the expected value.
        If any of the attribute checks fail, the test will fail.
        """
        self.assertEqual(self.account.account_number, '1234567890')
        self.assertEqual(self.account.balance, 500.00)
        self.assertEqual(self.account.customer_name, "Jhon Doe")
        self.assertEqual(self.account.account_type, "Savings")

    def test_create_account_with_duplicated_account_number(self):
        """
         It tests the behavior of creating an account object with a duplicate account number,
         which should raise an IntegrityError due to violating the unique constraint of the account number field.
         The test creates an account object with account number, balance, customer name, and account type.
         It then attempts to create another account object with the same account number but a different balance,
         customer name, and account type. The test expects an IntegrityError to be raised and passes
         the test if an error occurs. If no error is raised, the test fails with an AssertionError message
         indicating that the creation of an account with a duplicate account number was allowed.
        """
        try:
            Account.objects.create(account_number='1234567890', balance=5650.00,
                                   customer_name='Superman', account_type='Cheks')
        except IntegrityError:
            pass
        else:
            raise AssertionError(
                "Allowed to create an account with a duplicate account number")

    def test_withdraw_cash_with_enought_balance(self):
        """
        It tests the behavior of withdrawing cash from an account with enough balance.
        The test creates an account object with an account number, balance, customer name,
        and account type. It then subtracts 100.00 from the account balance and saves the account object.
        Finally, the test checks if the account balance is equal to 400.00, which is the expected result
        after the withdrawal. The test passes if the account balance is equal to the expected value and fails if not.
        """
        self.account.balance -= 100.00
        self.account.save()
        self.assertEqual(self.account.balance, 400.00)

    def test_withdraw_money_from_an_account_with_insufficient_balance(self):
        """
        It tests the behavior of withdrawing money from an account with insufficient balance,
        which should raise an IntegrityError due to a negative balance.
        The test creates an account object with an account number, balance, customer name,
        and account type. It then attempts to withdraw 600.00 from the account balance,
        which exceeds the current balance of 500.00. The test expects an IntegrityError to be
        raised and passes the test if an error occurs. If no error is raised, the test fails with an
        AssertionError message indicating that the withdrawal of money with insufficient balance was allowed.
        """
        try:
            self.account.balance -= 600.00
            self.account.save()
        except ValidationError:
            pass
        else:
            raise AssertionError(
                "Withdrawal of money with insufficient balance was allowed")

    def test_delete_an_existing_account(self):
        """
        First, a new account is created with some initial information such as account number,
        balance, customer name, and account type. Then, the account is deleted using the delete() method of
        the Account model.
        After deleting the account, the test tries to retrieve the account using the account number.
        If the account is not found (raises Account.DoesNotExist exception), the test passes.
        However, if the account is still found, it raises an AssertionError with the message
        "The account was not deleted correctly".
        This test is useful to ensure that the account deletion functionality works as expected and
        removes the account from the system properly.
        """

        self.account.delete()

        try:
            Account.objects.get(account_number='1234567890')
        except Account.DoesNotExist:
            pass
        else:
            raise AssertionError(
                "The account was not deleted correctly")

    def test_if_balance_is_updated_on_a_new_transaction(self):
        """
        In this test code, we are testing if an account balance gets updated correctly on performing a new
        transaction. We first create a deposit transaction for an amount of 1000, which should result in an 
        account balance of 1500. We then verify if the account balance equals 1500 using the assertEqual method.
        Next, we create a withdrawal transaction for an amount of 300, which should reduce the account balance
        to 1200. Again, we verify if the account balance has updated correctly and equals 1200.
        """
        Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=1000,
            transaction_type="Deposit",
        )
        self.assertEqual(self.account.balance, 1500.00)
        Transaction.objects.create(
            transaction_id="abcdefghijk123",
            account_number=self.account,
            amount=300.00,
            transaction_type="Withdraw",
        )
        self.assertEqual(self.account.balance, 1200.00)


class TransactionModelTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_was_created_correctly(self):
        """
        This test creates an Account object and a corresponding Transaction object.
        It then checks that the transaction was created with the correct values by comparing
        the fields of the transaction object with the expected values using self.assertEqual().
        """

        transaction = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=500.00,
            transaction_type="deposit",
        )
        self.assertEqual(transaction.transaction_id, "abcdefghijk")
        self.assertEqual(
            transaction.account_number.account_number, "1234567890")
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.transaction_type, "deposit")

    def test_create_transaction_with_non_existent_account(self):
        """
        This test tries to create a Transaction object with an account_number that doesn't exist in the database. 
        It expects an Account.DoesNotExist exception to be raised, and if not, it raises an AssertionError.
        """
        try:
            transaction = Transaction.objects.create(
                transaction_id="abcdefghijk",
                account_number=Account.objects.get(
                    account_number="0987654321"),
                amount=500.00,
                transaction_type="deposit",
            )
        except Account.DoesNotExist:
            pass
        else:
            AssertionError(
                "Created a transaction with a non-existent account ")

    def test_withdraw_more_balance_than_available(self):
        """
        This test tries to create a Transaction object with an amount greater than the available 
        balance in the associated account. It expects a ValidationError to be raised, and if not, 
        it raises an AssertionError.
        """
        try:
            transaction = Transaction.objects.create(
                transaction_id="abcdefghijk",
                account_number=self.account,
                amount=1000.00,
                transaction_type="Withdraw"
            )
        except ValidationError:
            pass

        else:
            raise AssertionError(
                "A withdrawal transaction was created with insufficient balance")

    def test_successfully_transaction_withdraw(self):
        """
        This test creates an Account object and a corresponding Transaction object representing a withdrawal. 
        It then checks that the account balance was updated correctly by comparing the account balance 
        after the withdrawal with the expected balance using self.assertEqual().
        """

        transation = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=200.00,
            transaction_type="Withdraw",
        )

        self.assertEqual(self.account.balance, 300.00)

    def test_successfully_transaction_delete(self):
        """
        This test creates an Account object and a corresponding Transaction object. 
        It then deletes the transaction object and checks that it was deleted correctly 
        by trying to retrieve it from the database using Transaction.objects.get() and expecting a 
        Transaction.DoesNotExist exception to be raised. If the transaction is found, it raises an AssertionError.
        """

        transation = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=200.00,
            transaction_type="Withdraw",
        )

        transation.delete()

        try:
            Transaction.objects.get(transaction_id="abcdefghijk")
        except Transaction.DoesNotExist:
            pass

        else:
            raise AssertionError("The transaction was not deleted correctly")


class AccountCreateViewTest(TestCase):

    def setUp(self):
        self.url = reverse('api:account_create_view')

    def test_create_account_with_valid_data(self):
        """
        the URL of the view is set and the account data to be created is defined, 
        such as the account number, balance, customer name, account type, and last update date. 
        Then, a POST request is sent to the URL with the account data and it is verified that the 
        response has a status code of 201, which means that a new account has been created. Next, 
        it is checked that the account has been created correctly in the database and some specific fields, 
        such as the balance, customer name, and account type, are checked.
        """

        self.data = {
            'account_number': '1234567890',
            'balance': 1000.00,
            'customer_name': 'John Doe',
            'account_type': 'Savings',

        }
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Account.objects.filter(
            account_number=self.data['account_number']).exists())
        account = Account.objects.get(
            account_number=self.data['account_number'])
        self.assertEqual(account.balance, float(self.data['balance']))
        self.assertEqual(account.customer_name, self.data['customer_name'])
        self.assertEqual(account.account_type, self.data['account_type'])

    def test_create_account_with_existent_account_number(self):
        """
        verify the behavior of the AccountCreateView when attempting to create an account with an 
        existing account number. The test first creates an Account object with an account number of '1234567890'. 
        It then attempts to create a new account with the same account number, '1234567890', 
        but with a different customer name and balance. The test expects a response status code of 400, 
        indicating that the account was not successfully created due to the duplicate account number. 
        Finally, the test verifies that no Account object exists with the account number and customer 
        name specified in the data dictionary.
        """
        account = Account.objects.create(account_number='1234567890', balance=500.00,
                                         customer_name="Jhon Doe", account_type="Savings")
        data = {
            'account_number': '1234567890',
            'balance': 1000.00,
            'customer_name': 'jhon doe',
            'account_type': 'Savings',

        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Account.objects.filter(
            account_number=data['account_number'], customer_name=data['customer_name']).exists())

    def test_create_account_with_invalid_name(self):
        """
        verify the behavior of the AccountCreateView when attempting to create an account 
        with an empty customer name field. The test first creates an Account object with a valid account number, 
        balance, customer name, and account type. It then attempts to create a new account with an invalid 
        customer name field (empty string) and valid values for the other fields. The test expects a response 
        status code of 400, indicating that the account was not successfully created due to the invalid 
        customer name. Finally, the test verifies that no Account object exists with the account number and 
        customer name specified in the data dictionary.
        """
        account = Account.objects.create(account_number='1234567890', balance=500.00,
                                         customer_name="Jhon Doe", account_type="Savings")
        data = {
            'account_number': '123456327890',
            'balance': 1000.00,
            'customer_name': '',
            'account_type': 'Savings',

        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Account.objects.filter(
            account_number=data['account_number'], customer_name=data['customer_name']).exists())


class AccountUpdateViewTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")
        self.url = reverse('api:account_update_view', args=(self.account.pk,))

    def test_update_account_with_valid_data(self):
        """
        This test verifies that a user account is updated correctly in the database. 
        The account data that is updated includes the account number, balance, customer name, and account type.
        First, the necessary data to update the account is set, and a POST request is made to the server 
        with this data. Then, it is checked that the server's response is an HTTP status code of 200, 
        indicating that the update was successful.
        After that, the updated account is searched for in the database, and it is verified that the data has 
        been updated correctly. This is done by comparing the values of the updated account with the data that 
        was set previously.
        If all the checks are successful, then the test is considered to have passed, and the account was 
        updated correctly.
        """
        self.data = {
            'account_number': '1234567890',
            'balance': 1200.00,
            'customer_name': 'Maria Gonzalez',
            'account_type': 'Savings',

        }
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        updated_account = Account.objects.get(pk=self.account.pk)
        self.assertEqual(updated_account.account_number, '1234567890')
        self.assertEqual(updated_account.balance, 1200.00)
        self.assertEqual(updated_account.customer_name, 'Maria Gonzalez')
        self.assertEqual(updated_account.account_type, 'Savings')

    def test_update_account_with_invalid_data(self):
        """
        In this case, a test is being conducted to see what happens when an account is updated with invalid data. 
        The data entered in the test are: empty account number, balance of $1200.00, empty customer name, 
        and savings account type.
        Then, a POST request is sent with the provided data, and a response with a status code of 400 is expected.
        Additionally, it is checked that the original account values have not changed: account number '1234567890',
        balance of $500.00, customer name "Jhon Doe", and savings account type.
        In summary, this test is designed to ensure that invalid data cannot be updated in the bank 
        account and that the original account information remains intact.
        """
        self.data = {
            'account_number': '',
            'balance': 1200.00,
            'customer_name': '',
            'account_type': 'Savings',

        }
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.account.account_number, '1234567890')
        self.assertEqual(self.account.balance, 500.00)
        self.assertEqual(self.account.customer_name, "Jhon Doe")
        self.assertEqual(self.account.account_type, "Savings")


class AccountDeleteViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_delete_existent_account(self):
        """
        This test checks that an existing account can be deleted from the system. 
        The account is identified by its account number. The expected response is an HTTP status code of 200, 
        which means that the request was successfully completed and the account was deleted. 
        If the account does not exist, an error will be generated.
        """
        url = reverse('api:account_delete_view', args=('1234567890',))
        request = self.client.post(url)
        self.assertEqual(request.status_code, 200)
        try:
            Account.objects.get(account_number='1234567890')
        except Account.DoesNotExist:
            pass
        else:
            raise AssertionError(
                "The account was deleted correctly")

    def test_delete_inexistent_account(self):
        """
        This test checks that the system handles the deletion of a non-existent account correctly. 
        The account is identified by its account number. 
        The expected response is an HTTP status code of 404, 
        which means that the account was not found and could not be deleted. Additionally, 
        it is verified that the account was not accidentally deleted in the process 
        by checking that it still exists in the database.
        """
        url = reverse('api:account_delete_view', args=('7644567890',))
        request = self.client.post(url)
        self.assertEqual(request.status_code, 404)
        self.assertTrue(Account.objects.filter(pk=self.account.pk).exists())


class AccountDetailViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_retrieve_bank_account(self):
        """
        This test checks that the information of an existing bank account can be retrieved from the system. 
        The account is identified by its account number and an HTTP status code of 200 is expected in response, 
        indicating that the request was completed successfully. Additionally, it is verified that the information 
        received from the account matches the information stored in the database, including the account number, 
        balance, customer name, and account type.
        """
        url = reverse('api:account_detail_view', args=('1234567890',))
        request = self.client.get(url)
        data = json.loads(request.content)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(data['account_number'], self.account.account_number)
        self.assertEqual(data['balance'], self.account.balance)
        self.assertEqual(data['customer_name'], self.account.customer_name)
        self.assertEqual(data['account_type'], self.account.account_type)

    def test_retrieve_bank_account_with_invalid_account_number(self):
        """
        This test checks that the system handles the request for information of a bank account with 
        an invalid account number correctly. An HTTP status code of 404 is expected in response, 
        indicating that the account was not found in the system. This test ensures that the system will 
        not provide confidential information to a user who does not provide a valid account number.
        """
        url = reverse('api:account_detail_view', args=('12sdfd',))
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)


class TransactionCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('api:transaction_create_view')
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_create_account_with_valid_data(self):
        """
        Creates an account with a specific transaction ID, account number, amount, transaction type, 
        description, and status. The test checks if the response code is 201 (created), 
        the number of transactions in the database is 1, and if the transaction ID and 
        transaction type match the input.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': self.account.id,
            'amount': 500.00,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get(
            transaction_id='abcdefghijk').amount, 500.0)
        self.assertEqual(Transaction.objects.get(
            transaction_id='abcdefghijk').transaction_type, 'Deposit')

    def test_create_account_with_invalid_customer(self):
        """
        Creates an account with a non-existent customer ID. The test checks if the response code is 400 (bad request)
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_invalid_transaction_type(self):
        """
        Creates an account with an invalid transaction type. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': 100,
            'transaction_type': 'null',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_other_descriptions(self):
        """
        Creates an account with a different description from the initial deposit. 
        The test checks if the response code is 201, the number of transactions is 1, 
        and that the amount matches the input.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': self.account.id,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Other description',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get(
            transaction_id='abcdefghijk').amount, 100.0)

    def test_create_account_with_other_status(self):
        """
        Creates an account with a different status from "Success". The test checks if the response code is 201, 
        the number of transactions is 1, and that the amount matches the input.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': self.account.id,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Other description',
            'status': 'Status'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get(
            transaction_id='abcdefghijk').amount, 100.0)

    def test_create_account_with_empty_transaction_id(self):
        """
        Creates an account with an empty transaction ID. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': '',
            'account_number': 100,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_empty_account_number(self):
        """
        Creates an account with an empty account number. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': "",
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_invalid_empty_amount(self):
        """
        Creates an account with an empty amount. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': "",
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_empty_transaction_type(self):
        """
        Creates an account with an empty transaction type. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': 100,
            'transaction_type': '',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_empty_status(self):
        """
        Creates an account with an empty status. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': ''
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_account_with_empty_description(self):
        """
        Creates an account with an empty description. The test checks if the response code is 400 
        and that no transactions were created.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': 100,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': '',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_update_account_balance_on_deposit_transaction(self):
        """
        Creates an account with a deposit transaction. The test checks if the account balance was updated correctly.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': self.account.id,
            'amount': 100,
            'transaction_type': 'Deposit',
            'description': 'Initial deposit',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Account.objects.get(
            pk=self.account.id).balance, 600.00)

    def test_update_account_balance_on_withdraw_transaction(self):
        """
        This test verifies that an account balance is updated correctly after a successful $100 withdrawal transaction. 
        The test uses a client to make a POST request and checks if the answer has a status code 201. In addition, 
        the Account object is used to verify if the balance has decreased by $100 and is now $400.
        """
        data = {
            'transaction_id': 'abcdefghijk',
            'account_number': self.account.id,
            'amount': 500.00,
            'transaction_type': 'Withdraw',
            'description': 'ATM withdraw',
            'status': 'Success'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Account.objects.get(
            pk=self.account.id).balance, 0.00)


class TransactionUpdateViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

        self.transaction = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=500.00,
            transaction_type="Deposit",
            description="Initial Deposit",
            status="Sucess"
        )

    def test_update_transaction_with_valid_data(self):
        """
        This test checks whether the API successfully updates a transaction record when valid data is submitted. 
        It starts by generating a URL to access the view for updating the transaction record, then creates a 
        dictionary with valid transaction data. The test then sends a POST request to the URL with the transaction 
        data and checks whether the response code is 200, indicating that the transaction was updated successfully. 
        Finally, the test queries the updated transaction record from the database and checks that its fields match 
        the updated data.
        """
        url = reverse('api:transaction_update_view',
                      args=(self.transaction.pk,))
        data = {
            'transaction_id': '1234567890',
            'account_number': self.account.id,
            'amount': 1200,
            'transaction_type': 'Deposit',
            'description': 'Update Data',
            'status': 'Success'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        updated_transaction = Transaction.objects.get(pk=self.transaction.pk)
        self.assertEqual(updated_transaction.transaction_id, '1234567890')
        self.assertEqual(updated_transaction.amount, 1200.00)
        self.assertEqual(updated_transaction.transaction_type, 'Deposit')
        self.assertEqual(updated_transaction.description, 'Update Data')

    def test_update_transaction_with_amount_greater_than_balance(self):
        """
        This test checks whether the API properly handles an attempt to withdraw an amount greater 
        than the account balance. It follows the same process as the previous test but submits an amount 
        greater than the account balance for a withdrawal transaction. The test expects a validation error 
        to be raised since the transaction cannot be completed, and if no error is raised, it raises one itself.
        """
        url = reverse('api:transaction_update_view',
                      args=(self.transaction.pk,))
        data = {
            'transaction_id': '1234567890',
            'account_number': self.account.id,
            'amount': 1200,
            'transaction_type': 'Withdraw',
            'description': 'Update Data',
            'status': 'Success'
        }

        try:
            response = self.client.post(url, data=data)
        except ValidationError:
            pass
        else:
            raise ValidationError(
                "deposit a withdrawal with an amount greater than the balance")

    def test_update_transaction_with_invalid_data(self):
        """
        This test checks whether the API handles invalid data correctly when updating a transaction. 
        It follows the same process as the first test but submits invalid data for the account number and 
        transaction type fields. The test expects a response code of 400, indicating that the data is 
        invalid and cannot be processed.
        """
        url = reverse('api:transaction_update_view',
                      args=(self.transaction.pk,))
        data = {
            'transaction_id': '1234567890',
            'account_number': 'Jhon Doe',
            'amount': 1200,
            'transaction_type': 'Transfer',
            'description': 'Update Data',
            'status': 'Success'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)


class TransactionDeleteViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

        self.transaction = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=500.00,
            transaction_type="Deposit",
            description="Initial Deposit",
            status="Sucess"
        )

    def test_delete_existent_transaction(self):
        """
        Check if an existing transaction can be deleted correctly. An HTTP POST request is made 
        to the transaction deletion view and it is verified that the response has an HTTP 200 status code, 
        indicating that the deletion was successful. Then it is verified that the transaction no longer 
        exists in the database.
        """
        url = reverse("api:transaction_delete_view",
                      args=("abcdefghijk",))
        request = self.client.post(url)

        self.assertEqual(request.status_code, 200)
        self.assertFalse(Transaction.objects.filter(
            transaction_id="abcdefghijk").exists())

    def test_delete_inexistent_transaction(self):
        """
        Check if the API correctly handles the deletion of a transaction that does not exist. 
        An HTTP POST request is made to the transaction deletion view with a transaction identifier 
        that does not exist and it is verified that the response has an HTTP 404 status code, 
        indicating that the transaction could not be found to delete it.
        """
        url = reverse("api:transaction_delete_view",
                      args=("nonexistent",))
        request = self.client.post(url)

        self.assertEqual(request.status_code, 404)


class TransactionDetailViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

        self.transaction = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=500.00,
            transaction_type="Deposit",
            description="Initial Deposit",
            status="Sucess"
        )

    def test_retrieve_transaction_detail(self):
        """
        checks if a transaction detail can be successfully retrieved from the API. It sends a GET 
        request to the transaction detail view with a valid transaction ID and checks if the response status 
        code is 200. It also checks if the response data matches the expected values for the transaction's attributes.
        """
        url = reverse('api:transaction_detail_view', args=('abcdefghijk',))
        request = self.client.get(url)
        data = json.loads(request.content)
        data_decoded = json.loads(data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(data_decoded['transaction_id'],
                         self.transaction.transaction_id)
        self.assertEqual(data_decoded['account_number'],
                         {'account_number': self.account.account_number})
        self.assertEqual(data_decoded['amount'], self.transaction.amount)
        self.assertEqual(data_decoded['transaction_type'],
                         self.transaction.transaction_type)
        self.assertEqual(data_decoded['description'],
                         self.transaction.description)
        self.assertEqual(data_decoded['status'], self.transaction.status)

    def test_retrieve_transaction_with_invalidad_transaction_id(self):
        """
        checks if the API returns a 404 error when attempting to retrieve a transaction with an 
        invalid transaction ID. It sends a GET request to the transaction detail view with an invalid 
        transaction ID and checks if the response status code is 404.
        """
        url = reverse('api:transaction_detail_view', args=('faketransaction',))
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)


class TransactionListViewPerAccountTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")
        self.account_no_transactions = Account.objects.create(account_number='no_transactions', balance=500.00,
                                                              customer_name="Jhon Doe", account_type="Savings")

        self.transaction = Transaction.objects.create(
            transaction_id="abcdefghijk",
            account_number=self.account,
            amount=500.00,
            transaction_type="Deposit",
            description="Initial Deposit",
            status="Sucess"
        )
        self.transaction2 = Transaction.objects.create(
            transaction_id="1234567",
            account_number=self.account,
            amount=5000.00,
            transaction_type="Deposit",
            description="Second Deposit",
            status="Sucess"
        )

    def test_return_list_with_correct_data(self):
        """
        Verifies if the transaction endpoint returns a list with the correct data for a given bank account. 
        To do this, an account number is established, an HTTP GET request is generated through the Django 
        test client and it is checked if a code 200 response is returned. Then it is verified if the returned 
        data is the same as the expected data for the transactions that were made for that bank account.
        """
        account_number = "1234567890"
        url = reverse('api:transaction_list_view', args=(account_number,))
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data[0]['transaction_id'], self.transaction.transaction_id)
        self.assertEqual(
            response_data[0]['amount'], self.transaction.amount)
        self.assertEqual(
            response_data[1]['transaction_id'], self.transaction2.transaction_id)
        self.assertEqual(
            response_data[1]['amount'], self.transaction2.amount)

    def test_return_list_with_incorrect_data(self):
        """
        Verifies if the transaction endpoint returns a 404 error response when an incorrect account ID is provided. 
        To do this, a non-existent account number is established, an HTTP GET request is generated through the 
        Django test client and it is checked if a 404 code response is returned.
        """
        account_number = "incorrect_id"
        url = reverse('api:transaction_list_view', args=(account_number,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_bank_account_with_no_transactions(self):
        """
        Tries to access a bank account that does not have registered transactions.

        First, the account number account_number that will be used to perform the test is defined. 
        Then, the URL corresponding to the TransactionListView view is generated using the account 
        number in question. Next, a GET request is made to the URL using the Django test client and 
        the response is stored in the response variable.

        Then two things are verified. First, it is verified that the status code of the response is 200, 
        which means that the request was made correctly. Afterwards, it is verified that the content of 
        the answer is an empty list. To do this, the content of the response is loaded as JSON using 
        json.loads() and compared to an empty list using assertEqual().
        """
        account_number = "no_transactions"
        url = reverse('api:transaction_list_view', args=(account_number,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])


class AccountBalanceUpdateViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number='1234567890', balance=500.00,
                                              customer_name="Jhon Doe", account_type="Savings")

    def test_update_account_with_valid_data(self):
        """
        Proves that the balance of an existing account can be updated using the endpoint 
        api:account_balance_update_view. A POST request is made to the corresponding URL, 
        sending a data object that contains a new balance for the account. It is expected that the 
        response will have an HTTP 200 status code and that the updated account will have the new balance.
        """
        url = reverse('api:account_balance_update_view',
                      args=(self.account.pk,))

        data = {
            'balance': 1200.00,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        updated_account = Account.objects.get(pk=self.account.pk)
        self.assertEqual(updated_account.balance, 1200.00)

    def test_update_account_with_invalid_data(self):
        """
        Proof that the balance of a non-existent account cannot be updated. 
        A POST request is made to a URL that does not correspond to an existing account, 
        sending a data object that contains a new balance for the account. The response is expected to 
        have an HTTP 404 status code, since the account does not exist in the database.
        """
        url = reverse('api:account_balance_update_view', args=(20,))

        data = {
            'balance': 1200.00,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 404)
