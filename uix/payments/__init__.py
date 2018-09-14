from .info import PaymentsInfo
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from .select import PaymentsSelectClient


class Payments(Screen):
    """Screen and screen manager for payments."""
    def __init__(self, **kwargs):
        """Initializion method."""
        super().__init__(**kwargs)
        # Create its own screen manager and add screens.
        self.sm = ScreenManager(transition=SwapTransition())
        self.sm.add_widget(PaymentsSelectClient(name='select'))
        self.sm.add_widget(PaymentsInfo(name='info'))
        self.add_widget(self.sm)

    def on_pre_enter(self):
        """Update informations of the first screen of the manager."""
        self.sm.current_screen.on_pre_enter()
