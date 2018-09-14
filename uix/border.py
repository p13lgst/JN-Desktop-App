from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class Border(Widget):
    """Base simple border widget."""


class BorderedLabel(Label, Border):
    """Label with border."""


class BorderedButton(Button, Border):
    """Button with border."""
