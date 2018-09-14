from .client import NewOrderClient
from .itens import NewOrderItens
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from .last import NewOrderLast


class NewOrder(Screen):
    """Main screen widget of making a new order."""

    def __init__(self, **kwargs):
        """Initializion method creating screen manager and adding all the
        screens to it.
        """
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=SwapTransition())
        self.sm.add_widget(NewOrderItens(name="itens"))
        self.sm.add_widget(NewOrderClient(name="client"))
        self.sm.add_widget(NewOrderLast(name="last"))
        self.add_widget(self.sm)
