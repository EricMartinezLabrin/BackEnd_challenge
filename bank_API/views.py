# Django
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.core.serializers.json import DjangoJSONEncoder

# Local
from bank_API.models import Account, Transaction

# Python
import json


class AccountCreateView(CreateView):
    """
    Allows you to create a new bank account. In the form_valid method, the view validates the received 
    form and if it is valid, creates a new instance of the account model and saves it in the database. 
    Then, it returns a JSON response with the data of the newly created account and a status code 201 (created).

    In case the form is not valid, the view returns a JSON response with the errors of the form and a 
    status code 400 (incorrect request) in the form_invalid method.
    """
    model = Account
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'id': self.object.id,
            'account_number': self.object.account_number,
            'balance': self.object.balance,
            'customer_name': self.object.customer_name,
            'account_type': self.object.account_type,
        }

        return JsonResponse(data, status=201)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class AccountUpdateView(UpdateView):
    """
    Is used to update the data of an existing account in the system. 
    The view uses the Account model and allows you to update all the fields in the account. 
    If the form data is valid, the view returns a JSON response with the updated account data and a 
    200 status code. If the form data is not valid, the view returns a JSON response with the errors and a 
    400 status code.
    """
    model = Account
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'id': self.object.id,
            'account_number': self.object.account_number,
            'balance': self.object.balance,
            'customer_name': self.object.customer_name,
            'account_type': self.object.account_type,
        }

        return JsonResponse(data, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class AccountDeleteView(DeleteView):
    """
    Is responsible for deleting a specific bank account. Receive a POST request and use the 
    get_object method to obtain the corresponding account object through the account number 
    provided in the URL arguments. If the account is found, a JSON response is deleted and 
    returned with a message indicating that the deletion has been successful and an HTTP 200 status code.
    """
    model = Account

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, account_number=self.kwargs['account_number'])
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'message': 'Object deleted successfully.'}
        return JsonResponse(data, status=200)


class AccountDetailView(DetailView):
    """
    Shows information about a specific bank account. Retrieve the account through the account number in the 
    URL and return the account information in JSON format with an HTTP response status code of 200. 
    The account information includes the account number, the balance, the name of the customer, 
    the type of account, the date of creation of the account and the date of the last update. 
    If the account does not exist, it returns a 404 error.
    """
    model = Account

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, account_number=self.kwargs['account_number'])
        return obj

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        data = {
            "account_number": obj.account_number,
            "balance": obj.balance,
            "customer_name": obj.customer_name,
            "account_type": obj.account_type,
            "account_creation": obj.account_creation,
            "last_update": obj.last_update,
        }
        return JsonResponse(data, status=200)


class TransactionCreateView(CreateView):
    """
    Allows you to create a new transaction in the database through an HTTP POST request. 
    The view uses a predefined form to validate the information sent by the client, if the form is valid, 
    the view saves the data in the database and returns a JSON response with the details of the new 
    transaction and a status code 201 (created). If the form is invalid, the view returns a 
    JSON response with validation errors and a status code 400 (incorrect request).
    """
    model = Transaction
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'transaction_id': self.object.transaction_id,
            'account_number': self.object.account_number.id,
            'amount': self.object.amount,
            'transaction_type': self.object.transaction_type,
            'timestamp': self.object.timestamp,
            'description': self.object.description,
            'status': self.object.status
        }
        return JsonResponse(data, status=201)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class TransactionUpdateView(UpdateView):
    """
    actualiza los detalles de una transacción existente en la base de datos. 
    Esta vista utiliza un modelo de transacción y acepta todos los campos del modelo. 
    Cuando se recibe un formulario válido, se guarda la instancia de la transacción y se 
    devuelve una respuesta JSON con los detalles actualizados de la transacción y un código de estado 200. 
    Si se recibe un formulario no válido, se devuelven los errores del formulario como una respuesta 
    JSON con un código de estado 400.
    """
    model = Transaction
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'transaction_id': self.object.transaction_id,
            'account_number': self.object.account_number.id,
            'amount': self.object.amount,
            'transaction_type': self.object.transaction_type,
            'description': self.object.description,
            'status': self.object.status
        }

        return JsonResponse(data, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class TransactionDeleteView(DeleteView):
    """
    Is responsible for handling requests to delete objects from the database. 
    In particular, it is designed to handle requests to remove objects of type Transaction.

    To do this, the view implements a get_object() method that obtains the transaction object 
    corresponding to the current deletion request. Then, in the post() method, the object is deleted 
    and a JsonResponse object is returned that indicates that the operation has been performed correctly, 
    along with a 200 status code.
    """
    model = Transaction

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, transaction_id=self.kwargs['transaction_id'])
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'message': 'Object deleted successfully.'}
        return JsonResponse(data, status=200)


class TransactionDetailView(DetailView):
    """
    Shows detailed information about a transaction using the Transaction model. 
    First, the object from the transaction is retrieved and serialized into a custom JSON object using 
    a custom encoder that handles objects of type Account. Then, the JSON object is returned in response 
    to the request in secure format. If the JSON object cannot be serialized, an appropriate error message 
    is returned.
    """
    model = Transaction

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, transaction_id=self.kwargs['transaction_id'])
        return obj

    def render_to_response(self, context, **response_kwargs):
        def custom_encoder(o):
            if isinstance(o, Account):
                return {'account_number': o.account_number}
            raise TypeError(
                f'Object of type {o.__class__.__name__} is not JSON serializable')
        obj = self.get_object()
        data = {
            "transaction_id": obj.transaction_id,
            "account_number": obj.account_number,
            "amount": obj.amount,
            "transaction_type": obj.transaction_type,
            "description": obj.description,
            "status": obj.status,
        }
        json_data = json.dumps(
            data, cls=DjangoJSONEncoder, default=custom_encoder)
        return JsonResponse(json_data, status=200, safe=False)
