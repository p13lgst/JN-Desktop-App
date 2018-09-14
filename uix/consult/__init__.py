from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition

from .select import ConsultSelectClient
from .info import ClientInfo
from .details import OrderDetails

class Consult(Screen):
    """Main screen widget of consult clients and orders."""

    def __init__(self, **kwargs):
        """Initializion method creating screen manager and adding all the
        screens to it.
        """
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=SwapTransition())
        self.sm.add_widget(ConsultSelectClient(name='select'))
        self.sm.add_widget(ClientInfo(name='info'))
        self.sm.add_widget(OrderDetails(name='details'))
        self.add_widget(self.sm)

    def on_pre_enter(self):
        """Update the first screen before entering."""
        self.sm.current_screen.on_pre_enter()
