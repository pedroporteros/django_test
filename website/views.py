from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from website.models import UserPoints
from website.forms import DepositForm
from website.services import make_deposit

# Create your views here.

# En esta clase se crean las vistas
class TransactionListView(ListView):
    model = UserPoints # Se define el modelo a utilizar
    context_object_name = 'transaction_data' # Se define el nombre del contexto
    
    # Se sobreescribe el metodo get_queryset para obtener los datos de la base de datos
    def get_querysey(self):
        return UserPoints.objects.all()
    
    # Se sobreescribe el metodo render_to_response para renderizar la respuesta
    def render_to_response(self, context, **response_kwargs):
        transactions = ''
        for transaction in context['transaction_data']:
            transactions += f'''<tr>
                            <td>{transaction.user}</td>
                            <td>{transaction.reward_transaction.description}</td>
                            <td>{transaction.amount_given}</td>
                            <td>{transaction.amount_used}</td>
                            <td>{transaction.amount_remaining}</td>
                            <td>{transaction.reward_transaction.date_of_transaction}</td>
                            <td>{transaction.expires_on}</td>
                            </tr>'''
        
        return HttpResponse(f'''<html><body><table>
                            <tr>
                            <th>User</th>
                            <th>Description</th>
                            <th>Amount Given</th>
                            <th>Amount Used</th>
                            <th>Amount Remaining</th>
                            <th>Date of Transaction</th>
                            <th>Expires On</th>
                            </tr>
                            {transactions}
                            </table></body></html>''')
     
# En esta clase se crea la vista para la creacion de un deposito   
class DepositView(TemplateView):
    template_name = 'website/deposit.html'
    
    # Se sobreescribe el metodo post para procesar la informacion del formulario
    def post(self, request):
        form = DepositForm(request.POST)
        
        if form.is_valid():
            user = form.cleaned_data.get('user')
            amount = form.cleaned_data.get('amount')
            description = form.cleaned_data.get('description')
            expires_on = form.cleaned_data.get('expires_on')
            
            make_deposit(user, amount, expires_on, description)
            
        return redirect('transactions') # Se redirige a la vista de transacciones

    # Se sobreescribe el metodo get_context_data para obtener el contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepositForm()
        return context