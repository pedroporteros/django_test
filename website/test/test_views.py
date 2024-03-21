from django.test import TestCase, RequestFactory
from django.urls import reverse
from website.models import SavingsTransaction, UserPoints
from django.contrib.auth.models import User

from website.views import MyBalanceView

# Create your tests here.

# En esta clase se crean los tests para las vistas
class TestViews(TestCase):
    fixtures = ['users.json']
    
    # Se sobreescribe el metodo setUp para crear un usuario y un deposito de puntos
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = User.objects.get(pk=1)
        deposit = SavingsTransaction.create_points_deposit_transaction(self.test_user, 154.44, 'Test Transaction')
        
        points = UserPoints.deposit_points(self.test_user, deposit)
    
    
    def test_transaction_list_view(self):
        url = reverse('transactions')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertInHTML('Test Transaction', resp.content.decode())
        self.assertInHTML('154.4400', resp.content.decode())
        
    # def test_deposit_view(self):
    #     url = reverse('deposit')
    #     payload = {
    #         'user': 1,
    #         'amount': 10,
    #         'description': 'post test deposit view'
    #     }
    #     resp = self.client.post(url, payload, follow=True)
    #     self.assertEqual(resp.status_code, 200, 'desposit view failed')
    #     self.assertInHTML('post test deposit view', resp.content.decode()) 
        
    # def test_deposit_expired_view(self):
    #     url = reverse('deposit')
    #     payload = {
    #         'user': 1,
    #         'amount': 10,
    #         'description': 'post test deposit view',
    #         'expires_on_month': 12,
    #         'expires_on_day': 1,
    #         'expires_on_year': 2023
    #     }
    #     resp = self.client.post(url, payload, follow=True)
    #     self.assertEqual(resp.status_code, 200, 'desposit view failed')
    #     self.assertInHTML('2023-12-01', resp.content.decode())
    
    def test_balance_view(self):
        url = reverse('balance')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200, 'balance view failed')
        
    def test_my_balance_view(self):
        url = reverse('mybalance')
        request = self.factory.get(url)
        request.user = self.test_user
        resp = MyBalanceView.as_view()(request)
        resp.render()
        self.assertEqual(resp.status_code, 200, 'my balance view failed')
        self.assertInHTML('test@gmail.com/154.44', resp.content.decode())
        
    def test_purchase_view(self):
        url = reverse('purchase')
        payload = {
            'user': 1,
            'amount': 11,
            'description': 'post test purchase view'
        }
        resp = self.client.post(url, payload, follow=True)
        self.assertEqual(resp.status_code, 200, 'purchase view failed')
        self.assertInHTML('143.44', resp.content.decode())