from db import Iten
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from .popups import ErrorPopup, SuccessPopup
from util.brl import format_brl, parse_brl


class Prices(Screen):
    """Screen with the prices and options to edit and erase them."""

    def on_pre_enter(self):
        """Update the itens before entering screen."""
        # Get the itens from the session
        app = App.get_running_app()
        itens = app.session.query(Iten).all()

        # Parse the itens and update the RecycleView data
        itens = [{'name': i.name, 'price': format_brl(i.price)} for i in itens]
        self.ids['itens'].data = itens

    def new_iten(self):
        """Initialize and open the popup to add a new iten."""
        NewIten().open()

    def edit(self, name):
        """Initialize and open the popup to edit the price of the iten that was
        specified by the name.
        """
        EditPrice(name).open()

    def delete(self, name):
        """Delete an iten."""
        # Get the session and delete the specified iten.
        app = App.get_running_app()
        app.session.query(Iten).filter(Iten.name == name).delete()
        app.session.commit()

        # Update prices.
        self.on_pre_enter()

        # Show that the operation succeeded.
        SuccessPopup("Iten apagado com sucesso!").open()


class NewIten(Popup):
    """Popup to add a new iten."""

    def add(self):
        """Add the iten."""
        # Get the informations from the inputs.
        name = self.ids['name'].text.strip()
        price = parse_brl(self.ids['price'].text.strip())

        app = App.get_running_app()

        # Check for errors.
        error = ''
        if not name:
            error = 'É necessário especificar um nome para o novo item!'

        elif not price:
            error = 'É necessário especificar um preço para o novo item!'

        elif app.session.query(Iten).filter(Iten.name == name).all():
            error = "Este item ja existe!"

        # If there is an error, show it and cancel adding.
        if error:
            ErrorPopup(error=error).open()
            return

        # If there is no error, add the iten.
        iten = Iten(name=name, price=price)
        app.session.add(iten)
        app.session.commit()

        # Show that the operation succeeded.
        SuccessPopup("Iten adicionado com sucesso!").open()

        # Update the screen information and exit the popup.
        app.prices.on_pre_enter()
        self.dismiss()


class EditPrice(Popup):
    """Popup to edit the price of an iten."""

    def __init__(self, name, **kwargs):
        """Initiatization method."""
        app = App.get_running_app()
        self.iten = app.session.query(Iten).filter(Iten.name == name).one()
        super().__init__(**kwargs)

    def save(self):
        """Save the informations to the database."""
        # Get the price from the input.
        price = parse_brl(self.ids['price'].text.strip())

        # Handle empty price.
        if not price:
            ErrorPopup('É necessário especificar um preço para o item!').open()
            return

        # Get the iten
        app = App.get_running_app()
        iten = app.session.query(Iten).filter(Iten.name == self.iten.name).one()

        # If the new price is the same, cancel and close the popup.
        if self.iten.price == price:
            self.dismiss()
            return

        # Update the iten
        iten.price = price
        app.session.commit()

        # Show that the operation succeeded.
        SuccessPopup("Preço atualizado com sucesso!").open()

        # Update the screen inormation and exit the popup.
        app.prices.on_pre_enter()
        self.dismiss()
