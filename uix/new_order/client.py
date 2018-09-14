import os
from db import Client
from ..border import BorderedButton
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from ..popups import ErrorPopup
from util import is_left_click


class NewClient(Popup):
    """Popup to add a new client."""

    def create(self):
        """Get information and continue."""
        name = self.ids['name'].text.strip()
        phone = self.ids['phone'].text.strip()

        # Check if it has a name or not.
        if not name:
            ErrorPopup('É necessário especificar um nome para o novo cliente!').open()
            return

        # Store information, close poupup and go to last screen.
        app = App.get_running_app()
        app.new_order.sm.client = {'name': name, 'phone': phone}
        app.new_order.sm.current = 'last'
        self.dismiss()


class NewOrderClient(Screen):
    """Screen to select or add a client."""

    # Used to make easier to create and open the popup from kv files.
    new_client_popup = NewClient

    def filter(self, name=''):
        """Filter the clients by name."""
        name = name.strip()
        app = App.get_running_app()

        query = app.session.query(Client.name, Client.id)

        # Filter if a name was specified.
        if name:
            query = query.filter(Client.name.ilike(f'%{name}%'))

        # Update clients.
        clients = [{'name': c[0], 'id': c[1]} for c in query.all()]
        self.ids['clients'].data = clients

    def clean(self):
        """Clean the informations on the screen to default."""
        self.ids['search'].text = ''
        self.filter()

    def on_pre_enter(self):
        """Clean before entering the screen."""
        self.clean()


class ExistentClient(BorderedButton):
    """Button to searched clients."""

    id = NumericProperty()
    name = StringProperty()

    def on_touch_down(self, touch):
        """Select this client and go to last part."""
        if is_left_click(self, touch):
            app = App.get_running_app()
            app.new_order.sm.client = {'id': self.id, 'name': self.name}
            app.new_order.sm.current = 'last'
