from website.models import UserPoints, SavingsTransaction

# Este metodo se encarga de crear un deposito de puntos 
def make_deposit(amount, description, user, expires_on=None):
    deposit = SavingsTransaction.create_points_deposit_transaction(user, amount, description)
    points = UserPoints.deposit_points(user, deposit, expires_on)
    return points