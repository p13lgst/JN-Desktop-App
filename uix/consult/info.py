from decimal import Decimal

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from ..popups import ErrorPopup, SuccessPopup

from util.brl import format_brl

from db import Client, Order, Payment


class ClientInfo(Screen):
    """Screen to show client informations."""

    def on_pre_enter(self):
        """Update informations before entering the screen."""
        client = self.manager.client
        total = sum(Decimal(i.total) for i in client.orders)
        paid = sum(Decimal(i.amount) for i in client.payments)
        orders = [{
        "order_id": order.id,
        "local": order.local,
        "delivered": order.delivered,
        "total": order.total
        } for order in client.orders]
        self.ids['name'].text = client.name
        self.ids['phone'].text = client.phone
        self.ids['total'].text = format_brl(total)
        self.ids['paid'].text = format_brl(paid)
        self.ids['orders'].data = reversed(orders)

    def show_order_details(self, id):
        """Go to order details screen."""
        app = App.get_running_app()
        self.manager.order = app.session.query(Order).filter(Order.id == id).one()
        self.manager.current = "details"

    def delete(self):
        """Delete a client and all his payments and orders."""
        app = App.get_running_app()
        id = self.manager.client.id
        app.session.query(Payment).filter(Payment.client_id == id).delete()
        app.session.query(Order).filter(Order.client_id == id).delete()
        app.session.query(Client).filter(Client.id == id).delete()
        app.session.commit()

        # Show that operation succeeded.
        SuccessPopup("Cliente apagado com sucesso!").open()

        # Go back to main menu.
        self.manager.current = 'select'
        self.manager.parent.manager.current = "menu"

    def edit(self):
        """Edit client."""
        EditClient(self.manager.client.id).open()


class EditClient(Popup):
    """Popup to edit a client."""

    def __init__(self, id, **kwargs):
        """Initializion method."""
        super().__init__(**kwargs)

        # Get the client.
        app = App.get_running_app()
        self.client = app.session.query(Client).filter(Client.id == id).one()

        # Update info.
        self.ids['name'].text = self.client.name
        self.ids['phone'].text = self.client.phone

    def save(self):
        """Save the client information."""
        # Get information.
        name = self.ids['name'].text.strip()
        phone = self.ids['phone'].text.strip()

        # Check if a name was specified.
        if not name:
            ErrorPopup('É necessário especificar um novo nome para o cliente!').open()
            return

        # Update the client.
        self.client.name = name
        self.client.phone = phone
        app = App.get_running_app()
        app.session.commit()

        # Update information of the current screen.
        app.consult.sm.client = self.client
        app.consult.sm.current_screen.on_pre_enter()

        # Show that the operation succeeded.
        SuccessPopup("Cliente editado com sucesso!").open()

        # Close the popup.
        self.dismiss()
