from db import Order
from kivy.app import App
from kivy.uix.screenmanager import Screen
from ..popups import ErrorPopup, SuccessPopup


class EditOrder(Screen):
    """Screen to edit information about an order."""

    def on_pre_enter(self):
        """Update informations before entering the screen."""
        app = App.get_running_app()
        query = app.session.query(Order)
        self.order = query.filter(Order.id == self.manager.order_id).one()
        self.ids['title'].text = f"Editar dados da encomenda {self.order.id}"
        self.ids['delivered'].state = "down" if self.order.delivered else "normal"
        self.ids['not_delivered'].state = "normal" if self.order.delivered else "down"
        self.ids['local'].text = self.order.local
        self.ids['info'].text = self.order.extra_info

    def save(self):
        """Save the changes."""
        # Check if the local is specified.
        local = self.ids['local'].text.strip()
        if not local:
            ErrorPopup('É necessário especificar o local da entrega!').open()
            return

        # Update informations and save
        self.order.local = local
        self.order.extra_info = self.ids['info'].text.strip()
        self.order.delivered = int(self.ids['delivered'].state == 'down')
        app = App.get_running_app()
        app.session.commit()

        # Show that the operation succeeded and go back to menu.
        SuccessPopup("Encomenda editada com sucesso!").open()
        self.manager.current = 'list'
        self.manager.parent.manager.current = 'menu'




    def delete(self):
        """Delete the iten."""
        app = App.get_running_app()
        app.session.query(Order).filter(Order.id == self.manager.order_id).delete()
        app.session.commit()

        # Show that the operation succeeded and go back to menu.
        SuccessPopup("Encomenda apagada com sucesso!").open()
        self.manager.current = 'list'
        self.manager.parent.manager.current = 'menu'
