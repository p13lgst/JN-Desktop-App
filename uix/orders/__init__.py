from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition

from .list import OrderList
from .edit import EditOrder

class Orders(Screen):
    """Screen and screen manager to update orders."""

    def __init__(self, **kwargs):
        """Initializion method."""
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=SwapTransition())
        self.sm.add_widget(OrderList(name="list"))
        self.sm.add_widget(EditOrder(name="edit"))
        self.add_widget(self.sm)

    def on_pre_enter(self):
        """Update first screen of the its manager."""
        self.sm.current_screen.on_pre_enter()
