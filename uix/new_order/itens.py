from db import Iten
from decimal import Decimal, InvalidOperation, Overflow
from ..border import BorderedButton
from kivy.app import App
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from ..popups import ErrorPopup, SuccessPopup
from util import is_left_click
from util.brl import format_brl, parse_brl


class ItenToAdd(BorderedButton):
    """Button that add an iten on click."""

    def __init__(self, iten, **kwargs):
        """Initialization method with style information."""
        super().__init__(**kwargs)
        self.text = iten.name
        self.iten = iten
        self.background_color = 0,0,0,1
        self.font_size = 25
        self.size_hint_y = None
        self.height = 60

    def on_touch_down(self, touch):
        """Add the iten if is a left click on the button."""
        if is_left_click(self, touch):
            app = App.get_running_app()
            app.new_order.sm.current_screen.add_iten(self.iten)
            app.new_order.sm.current_screen.add_iten_popup.dismiss()


class AddIten(Popup):
    """Popup to add an iten to the order."""

    def close_btn_touch(self, btn, touch):
        """Close and cancel."""
        if is_left_click(btn, touch):
            self.dismiss()

    def new_iten_btn_touch(self, btn, touch):
        """Add a new iten."""
        if is_left_click(btn, touch):
            self.dismiss()
            NewIten().open()

    def __init__(self, **kwargs):
        """Initialization method with style information."""
        super().__init__(**kwargs)
        self.title = "Adicionar Item"
        self.title_size = 25
        self.title_align = 'center'
        self.size_hint = .7, .7
        self.content = BoxLayout(orientation='vertical')
        self.grid = BoxLayout(orientation="vertical", size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.grid)
        self.content.add_widget(scroll)
        buttons = BoxLayout(size_hint_y=None, height=60)

        buttons.add_widget(BorderedButton(
            background_color=(1,0,0,1),
            on_touch_down=self.close_btn_touch,
            text="Fechar",
            font_size=25,
            size_hint_y=None,
            height=60
        ))

        buttons.add_widget(BorderedButton(
            background_color=(0,1,0,1),
            text="Novo Item",
            on_touch_down=self.new_iten_btn_touch,
            font_size=25,
            size_hint_y=None,
            height=60
        ))

        self.content.add_widget(buttons)


    def on_open(self):
        """Get all the itens options."""
        app = App.get_running_app()
        for iten in app.session.query(Iten).all():
            self.grid.add_widget(ItenToAdd(iten))

    def on_dismiss(self):
        """Clear the current itens when closed."""
        self.grid.clear_widgets()


class NewOrderItens(Screen):
    """Screen to add the itesn to the order."""

    add_iten_popup = AddIten()

    def add_iten(self, iten):
        """Method to add the iten to the order if not added."""
        for i in self.ids['itens'].itens:
            if iten.name == i.name:
                return

        added_iten = AddedIten(name=iten.name, unity_price=iten.price)
        self.ids['itens'].itens.append(added_iten)

    def go_to_client(self):
        """Go select client."""
        itens = self.ids['itens'].export_itens()
        total = parse_brl(self.ids['total'].text)

        if not itens:
            ErrorPopup('É necessário adicionar no mínimo um item!').open()
        else:
            self.manager.itens = itens
            self.manager.total = total
            self.manager.current = 'client'

    def cancel(self):
        """Cancel the operation by cleaning and going back to menu."""
        app = App.get_running_app()
        app.sm.current = 'menu'
        for screen in app.new_order.sm.children:
            screen.clean()

    def clean(self):
        """Clean information on the screen."""
        app = App.get_running_app()
        self.ids['itens'].itens = []
        app.itens = []
        app.total = Decimal()


class NewIten(Popup):
    """Popup to add a new iten that it's not in the list."""

    def add(self):
        """Save the iten and add it to the order."""
        app = App.get_running_app()

        # Get information.
        name = self.ids['name'].text.strip()
        price = parse_brl(self.ids['price'].text.strip())
        # Check information.
        error = ''
        if not name:
            error = 'É necessário especificar um nome para o novo item!'
        elif not price:
            error = 'É necessário especificar um preço para o novo item!'
        elif app.session.query(Iten).filter(Iten.name == name).all():
            error = 'Este item ja existe!'

        # Show error if any.
        if error:
            ErrorPopup(error).open()
            return

        # Save the iten.
        iten = Iten(name=name, price=price)
        app.session.add(iten)
        app.session.commit()

        # Add it to the order.
        app.new_order.sm.current_screen.add_iten(iten)
        self.dismiss()


class AddedIten(BoxLayout):
    """Layout to the iten that was added."""
    quantity = ObjectProperty(Decimal())
    unity_price = ObjectProperty(Decimal())
    total_price = ObjectProperty(Decimal())

    def __init__(self, name, **kwargs):
        """Initializion method."""
        self.name = name
        super().__init__(**kwargs)

    def quantity_change(self):
        """Handle the change in quantity, validating and updating other values."""
        quantity_input = self.ids['quantity']
        quantity_text = quantity_input.text

        # Prevent errors for empty inputs.
        if not quantity_text:
            quantity_text = '0'

        # Prevent error parsing decimal because of commas.
        quantity_text = quantity_text.replace(',', '.')

        # Remove more than one dots.
        while quantity_text.count('.') > 1:
            quantity_text = quantity_text[::-1].replace('.', '', 1)[::-1]

        # Prevent the decimal dot to be removed when parsing decimal.
        if quantity_text[-1] == '.':
            quantity_input.text = quantity_text
        else:
            # If the exception InvalidOperation or Overflow is raised, do not
            # changed the values, making it not changed.
            try:
                self.quantity = abs(Decimal(quantity_text))
                self.total_price = self.quantity * self.unity_price
            except (InvalidOperation, Overflow):
                pass

            # Update the values.
            quantity_input.text = str(self.quantity)
            self.ids['total'].text = format_brl(self.total_price)
            self.parent.compute_total()

    def unity_price_change(self):
        """Handle the change in unity price, validating and updating other
        values.
        """
        # Get information.
        price_input = self.ids['unity_price']
        price_text = price_input.text

        # Check if changed and update information.
        if format_brl(self.unity_price) != price_text:
            self.unity_price = parse_brl(price_text)
            self.total_price = self.quantity * self.unity_price
            self.ids['total'].text = format_brl(self.total_price)
            self.ids['unity_price'].text = format_brl(self.unity_price)
            self.parent.compute_total()


    def total_change(self):
        """Handle the change in price, validating and updating other values."""
        # Get information.
        total_input = self.ids['total']
        total_text = total_input.text

        # Check if changed and update information.
        if format_brl(self.total_price) != total_text:
            self.total_price = parse_brl(total_text)
            self.ids['total'].text = format_brl(self.total_price)

            # Prevent division by zero.
            if self.quantity:
                self.unity_price = self.total_price / self.quantity
                self.ids['unity_price'].text = format_brl(self.unity_price)
            self.parent.compute_total()


class Itens(StackLayout):
    """Layout with all the added itens."""
    itens = ListProperty()

    def remove_iten(self, iten):
        """Remove an iten."""
        self.itens.remove(iten)

    def on_itens(self, iten, itens):
        """Update the itens when changed."""
        self.itens = sorted(itens, key=lambda x: x.name)
        self.clear_widgets()
        for iten in self.itens:
            self.add_widget(iten)

    def compute_total(self):
        """Calculate the total."""
        app = App.get_running_app()
        label = app.new_order.sm.current_screen.ids['total']
        label.text = format_brl(sum(iten.total_price for iten in self.itens))

    def export_itens(self):
        """Return all the valid added itens."""
        itens = []
        for iten in self.itens:
            if iten.quantity and iten.unity_price and iten.total_price:
                itens.append({'name': iten.name,
                              'price': iten.unity_price,
                              'quantity': iten.quantity})

        return itens
