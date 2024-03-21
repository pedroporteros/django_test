from django.test import TestCase
from django.contrib.auth.models import User
from website.models import SavingsTransaction
# Create your tests here.

# En esta clase se crean los tests para el modelo
class TestUser(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.test_user = User.objects.get(pk=1)
    
    def test_create_deposit_points_transaction(self):
        
        amount = 10
        description = 'Points Test1 Deposit'
        new_trasancion = SavingsTransaction.create_points_deposit_transaction(self.test_user, amount, description) 
        
        self.assertIsNotNone(new_trasancion, 'Deposit transaction not created')
        self.assertEqual(new_trasancion.user, self.test_user, 'User not matched')
        self.assertEqual(new_trasancion.amount, amount, 'Amount not matched')
        self.assertEqual(new_trasancion.description, description, 'Description not matched')
        self.assertEqual(new_trasancion.transaction_type, SavingsTransaction.DEPOSIT, 'Transaction type not matched')