from django.test import TestCase
from django.contrib.auth.models import User
from website.forms import PurchaseModelForm


# En esta clase se crean los tests para el formulario
class FormTest(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.test_user = User.objects.get(pk=1)
        
    def test_purchase_form(self):
        purchase_form = PurchaseModelForm(data={
            'user': self.test_user, 
            'amount': 10.0, 
            'description': 'Test Purchase'
        })
        self.assertTrue(purchase_form.is_valid())