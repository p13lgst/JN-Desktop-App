from .border import BorderedLabel, BorderedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from util import is_left_click


class ErrorPopup(Popup):
    """Default popup to show errors."""
    def __init__(self, error, **kwargs):
        """Initiatization method to setup all the style."""
        super().__init__(**kwargs)
        self.title = 'Erro!'
        self.title_align = 'center'
        self.title_size = 20
        self.size_hint = None, None
        self.size = 800, 200
        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(BorderedLabel(text=error, color=(1,1,1,1)))
        self.content.add_widget(BorderedButton(text="Fechar",
                                               background_color=(1,0,0,1),
                                               on_touch_down=self.close_btn_touch))

    def close_btn_touch(self, btn, touch):
        """Handle close touch."""
        if is_left_click(btn, touch):
            self.dismiss()


class SuccessPopup(Popup):
    """Default popup to show conclusion confirmation."""

    def __init__(self, message, **kwargs):
        """Initiatization method to setup all the style."""
        super().__init__(**kwargs)
        self.title = 'Sucesso!'
        self.title_align = 'center'
        self.title_size = 20
        self.size_hint = None, None
        self.size = 800, 200
        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(BorderedLabel(text=message, color=(1,1,1,1)))
        self.content.add_widget(BorderedButton(text="OK!",
                                               background_color=(0,1,0,1),
                                               on_touch_down=self.close_btn_touch))

    def close_btn_touch(self, btn, touch):
        """Handle close touch."""
        if is_left_click(btn, touch):
            self.dismiss()
