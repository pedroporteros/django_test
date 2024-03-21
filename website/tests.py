from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.db.transaction import TransactionManagementError
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

from website.models import SavingsTransaction
from website.services import make_deposit
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
        
# class PointsTransactionTest(TransactionTestCase):
#     fixtures = ['users.json']
    
#     def setUp(self):
#         self.test_user = User.objects.get(pk=1)
    
#     def test_purchase_with_points(self):
#         amount = 20
#         description = 'Points Test1 Purchase'
#         make_deposit(amount, description, self.test_user)
        
#         amount = 10
#         description = 'Points Test2 Purchase'
#         with self.assertRaises(TransactionManagementError):
#             make_deposit(amount, description, self.test_user)

class LiveTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options.binary_location = '/usr/bin/firefox'
        
        cls.selenium = webdriver.Firefox(options=firefox_options)
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_purchase(self):
        user = User.objects.get(pk=1)
        make_deposit(20, 'Test Live Deposit', user)
        self.selenium.get(f'{self.live_server_url}/points/purchase')
        user_select = Select(self.selenium.find_element(By.NAME, 'user'))
        user_select.select_by_value('1')
        amount_input = self.selenium.find_element(By.NAME, 'amount')
        amount_input.clear()
        amount_input.send_keys('10')
        desc_input = self.selenium.find_element(By.NAME, 'description')
        desc_input.send_keys('Test Live Purchase')
        self.selenium.find_element(By.XPATH, '//input[@value="Submit"]').click()
        
        WebDriverWait(self.selenium, 2).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        
        self.assertTrue('10.00' in self.selenium.page_source)