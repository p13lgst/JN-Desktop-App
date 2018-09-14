from datetime import date
from db import Client, Payment
from decimal import Decimal
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from ..popups import ErrorPopup, SuccessPopup
from util.brl import format_brl, parse_brl


class PaymentsInfo(Screen):
    """Screen with payment information from a client."""

    def on_pre_enter(self):
        """Update the information before entering the screen."""
        # Get the data
        client = self.manager.client
        payments = client.payments
        total = sum(Decimal(i.total) for i in client.orders)
        paid = sum(Decimal(i.amount) for i in payments)
        data = [{
            "payment_id": p.id,
            "amount": p.amount,
            "date": p.date.strftime("%d/%m/%Y")
        } for p in payments]

        # Set the data
        self.ids['name'].text = client.name
        self.ids['phone'].text = client.phone
        self.ids['total'].text = format_brl(total)
        self.ids['paid'].text = format_brl(paid)
        self.ids['remaining'].text = format_brl(total - paid)
        self.ids['payments'].data = reversed(data)

    def new_payment(self):
        """Initialize and open the popup for a new payment to the
        current client.
        """
        NewPayment(self.manager.client.id).open()

    def delete_payment(self, payment_id):
        """Delete the specified payment."""
        app = App.get_running_app()
        app.session.query(Payment).filter(Payment.id == payment_id).delete()
        app.session.commit()

        # Update the informations on the screen.
        self.on_pre_enter()

        # Show that the operation succeeded.
        SuccessPopup("Pagamento apagado com sucesso!").open()



class NewPayment(Popup):

    def __init__(self, client_id, **kwargs):
        """Initializion method."""
        super().__init__(**kwargs)
        self.client_id = client_id

        # Fill the date input
        self.ids['date'].text = date.today().strftime("%d/%m/%Y")

        # Variable to prevent double payment.
        self.done = False

    def register(self):
        """Register the new payment."""

        # Prevent double payment.
        if self.done:
            return
        self.done = True

        # Get amount and check if it is valid.
        amount = parse_brl(self.ids['amount'].text)
        if not amount:
            ErrorPopup("A quantidade não pode ser nula!").open()
            self.done = False
            return

        # Get and try to parse the date.
        date_tuple = self.ids['date'].text.strip().split('/')
        try:
            payment_date = date(*map(int,reversed(date_tuple)))
            print(payment_date)
        except (ValueError, TypeError):
            ErrorPopup("É necessário especificar a data válida do pagamento no formato DD/MM/AAAA!").open()
            self.done = False
            return

        app = App.get_running_app()
        client = app.payments.sm.client

        # Check values.
        paid = sum(Decimal(i.amount) for i in client.payments)
        total = sum(Decimal(i.total) for i in client.orders)
        if paid + amount > total:
            ErrorPopup("A quantidade paga não pode ser maior do que o que se deve!").open()
            self.done = False
            return

        # Register payment.
        app.session.add(Payment(amount=amount,date=payment_date ,client_id=self.client_id))
        app.session.commit()

        # Show that the operation succeeded.
        SuccessPopup("Pagamento registrado com sucesso!").open()

        # Close the popup and go back to main menu.
        self.dismiss()
        app.payments.sm.current = 'select'
        app.sm.current = 'menu'
