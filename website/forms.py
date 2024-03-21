from django import forms
from website.models import SavingsTransaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# En esta clase se crea el formulario para la creacion de una transaccion de compra
class PurchaseModelForm(forms.ModelForm):
    
    class Meta:
        model = SavingsTransaction
        fields = ['user', 'amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Purchase amount',
                                               'class': 'standard-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Purchase description',
                                                  'class': 'standard-area', 'rows': 10, 'cols': 80}),            
        }
    
    # Este metodo se encarga de validar que el monto sea mayor a 0  
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError('Amount must be greater than 0')
        return amount
    
    # Este metodo se encarga de validar que la descripcion no sea vacia
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError('Description can not be blank')
        return description
    
# En esta clase se crea el formulario para la creacion de una transaccion de deposito   
class DepositForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    amount = forms.FloatField(required=True, label='Deposit Amount')
    expires_on = forms.DateField(required=False, label='Expires On', widget=forms.SelectDateWidget())
    description = forms.CharField(required=False, label='Description of deposit', 
                                  widget=forms.Textarea(attrs={'placeholder':'Deposit description',
                                                               'class':'standard-area', 'rows': 10, 'cols': 80}))
    
    