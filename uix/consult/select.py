from db import Client
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen


class ConsultSelectClient(Screen):
    """Screen to select a client to consult."""

    def choose(self, id):
        """Choose a specific client by id and go to next screen."""
        app = App.get_running_app()
        self.manager.client = app.session.query(Client).filter(Client.id == id).one()
        self.manager.current = 'info'

    def filter(self, name=''):
        """Filter clients by name."""
        app = App.get_running_app()
        name = name.strip()

        query = app.session.query(Client.name, Client.id)

        # Filter if name was specified.
        if name:
            query = query.filter(Client.name.ilike(f'%{name}%'))

        # Update clients.
        clients = [{'name': c[0], 'client_id': c[1]} for c in query.all()]
        self.ids['clients'].data = clients


    def go_back(self):
        """Go back to menu."""
        app = App.get_running_app()
        app.sm.current = 'menu'

    def on_pre_enter(self):
        """Clean the informations on the screen to default."""
        self.ids['search'].text = ''
        self.filter()
