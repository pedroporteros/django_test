from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from datetime import datetime
from decimal import Decimal
# Create your models here.

# Esta clase se encarga de agregar los campos created_at y updated_at a los modelos que la hereden
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
# Esta clase se encarga de agregar los campos user, amount, description, date_of_transaction y transaction_type a los modelos que la hereden
class SavingsTransaction(TimeStampMixin):
    PURCHASE = 0
    DEPOSIT = 1
    REFUND = 2
    TRANSACTION_TYPES = [
        (PURCHASE, 'Purchase'),
        (DEPOSIT, 'Deposit'),
        (REFUND, 'Refund'),
    ]
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=19, decimal_places=4, default=0, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_of_transaction = models.DateField(auto_now_add=True)
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPES, 
        default=PURCHASE
    )
    
    def __str__(self):
        return f'{self.user} - {self.amount} - {self.description}'
    
    # Este metodo se encarga de crear una transaccion de deposito de puntos
    @classmethod
    def create_points_deposit_transaction(cls, user, amount, description):
        return cls.objects.create(user=user, amount=amount, description=description, transaction_type=SavingsTransaction.DEPOSIT)

# Esta clase se encarga de agregar los campos amount_given, amount_used, amount_remaining y expires_on a los modelos que la hereden   
class UserPoints(TimeStampMixin):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='points')
    reward_transaction = models.OneToOneField(SavingsTransaction, null=True, blank=True,
                                              on_delete=models.SET_NULL, related_name='point_deposit')
    amount_given = models.DecimalField(max_digits=19, decimal_places=4, default=0, null=True)
    amount_used = models.DecimalField(max_digits=19, decimal_places=4, default=0, null=True)
    amount_remaining = models.DecimalField(max_digits=19, decimal_places=4, default=0, null=True)
    purchase_transactions = models.ManyToManyField(SavingsTransaction, through='PointPurchaseTransaction')
    expires_on = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} - {self.amount_given} - {self.amount_remaining}'
    
    def get_amount_remaining(self) -> Decimal:
        return Decimal(str(self.amount_given - self.amount_used))
    
    def get_queryset(self):
        return self.__class__.objects.filter(id=self.id)
    
    def use_points(self, transaction:SavingsTransaction, amount:Decimal) -> Decimal:
        remaining = Decimal(0)
        try:
            obj = self.get_queryset().select_for_update().get()
            if amount <= obj.amount_remaining:
                PointPurchaseTransaction.objects.create(
                    purchase_transaction=transaction,
                    user_points=self,
                    amount_used=amount
                )
                
                obj.amount_used = Decimal(str(round(obj.amount_used + amount), 2))
            else:
                remaining = amount - obj.amount_remaining
                PointPurchaseTransaction.objects.create(
                    purchase_transaction=transaction,
                    user_points=self,
                    amount_used=obj.amount_remaining
                )
                
                obj.amount_used = Decimal(str(round(obj.amount_used + obj.amount_remaining), 2))
                obj.amount_remaining = Decimal(0)
            
            obj.save()
            return remaining
        except Exception as e:
            obj.purchase_transactions.remove(transaction)
            raise e
                
    
    # Este metodo se encarga de depositar puntos al usuario
    @classmethod
    def deposit_points(cls, user, reward_transaction:SavingsTransaction, expires_on=None):
        return cls.objects.create(user=user, reward_transaction=reward_transaction, amount_given=reward_transaction.amount, amount_remaining=reward_transaction.amount, expires_on=expires_on)
    
    @classmethod
    def calculated_remaining_points(cls, user):
        return cls.objects.filter(Q(expires_on__isnull=True) | Q(expires_on__gt=datetime.now().date()), user=user).aggregate(remaining_points=Sum('amount_remaining'))['remaining_points']
    
    @classmethod
    def get_available_points_deposits(cls, user):
        return cls.objects.filter(Q(expires_on__isnull=True) | Q(expires_on__gt=datetime.now().date()), user=user, amount_remaining__gt=0).order_by('expires_on', 'created_at')
    
    
class PointPurchaseTransaction(TimeStampMixin):
    purchase_transaction = models.ForeignKey(SavingsTransaction, null=True, on_delete=models.SET_NULL)
    user_points = models.ForeignKey(UserPoints, null=True, on_delete=models.SET_NULL)
    amount_used = models.DecimalField(max_digits=19, decimal_places=4, default=0, null=True)