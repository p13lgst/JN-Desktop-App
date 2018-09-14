from db import Client
from kivy.app import App
from kivy.uix.screenmanager import Screen


class PaymentsSelectClient(Screen):
    """Select the client to payments feature."""

    def choose(self, _id):
        """Choose the client and go to the next screen."""
        app = App.get_running_app()
        self.manager.client = app.session.query(Client).filter(Client.id == _id).one()
        self.manager.current = 'info'

    def filter(self, name=''):
        """Filter the clients by name."""
        name = name.strip()

        # Base query withour filtering
        app = App.get_running_app()
        query = app.session.query(Client.name, Client.id)

        # Filter name, if a non empty was specified.
        if name:
            query = query.filter(Client.name.ilike(f'%{name}%'))

        # Update RecycleView data
        clients = [{'name': c[0], 'client_id': c[1]} for c in query.all()]
        self.ids['clients'].data = clients

    def go_back(self):
        """Go back to menu."""
        app = App.get_running_app()
        app.sm.current = 'menu'

    def on_pre_enter(self, *args):
        """Update the information before entering the screen."""
        self.ids['search'].text = ''
        self.filter()
