from db import Client, Order
from kivy.app import App
from kivy.uix.screenmanager import Screen
from ..popups import ErrorPopup, SuccessPopup


class NewOrderLast(Screen):
    """Screen for the last part of making an order."""

    def finish(self):
        """Finish the order."""
        # Get the information.
        local = self.ids['local'].text.strip()
        info = self.ids['info'].text.strip()
        delivered = self.ids['delivered'].state == 'down'

        # Ensure local was given.
        if not local:
            ErrorPopup('É necessário especificar o local da entrega!').open()
            return

        app = App.get_running_app()

        # Get the client if already exists, otherwise create one.
        if 'id' in self.manager.client.keys():
            print('hi')
            query = app.session.query(Client)
            client = query.filter(Client.id == self.manager.client['id']).one()
        else:
            client = Client(
                name=self.manager.client['name'],
                phone=self.manager.client['phone']
            )
            app.session.add(client)
            app.session.commit()

        # Create the order
        order = Order(
            local=local,
            itens=self.manager.itens,
            total=self.manager.total,
            extra_info=info,
            client_id=client.id,
            delivered=delivered
        )
        app.session.add(order)
        app.session.commit()

        # Show that the operation succeeded and go back to main menu.
        SuccessPopup('Pedido realizado com sucesso').open()
        app.sm.current = 'menu'
        app.new_order.sm.current = 'itens'

        # Clean all the screens in this section.
        for screen in app.new_order.sm.children:
            screen.clean()

    def go_back(self):
        """Go back to select client."""
        self.manager.current = 'client'

    def clean(self):
        """Clean all information in the screen."""
        self.ids['info'].text = ''
        self.ids['local'].text = ''
        self.ids['delivered'].state = 'normal'
        self.ids['not_delivered'].state = 'down'
