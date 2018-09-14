#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Set the kivy home enviroment variable to the path of the foder .kivy
os.environ["KIVY_HOME"] = os.path.join(os.path.curdir, '.kivy')

# Set the window clear color to white.
from kivy.core.window import Window
Window.clearcolor = 1,1,1,1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SwapTransition
from uix.consult import Consult
from uix.menu import Menu
from uix.new_order import NewOrder
from uix.orders import Orders
from uix.payments import Payments
from uix.prices import Prices


from db import get_session

with open("style.kv", encoding='utf-8') as f:
    Builder.load_string(f.read())


class JnApp(App):

    def build(self):
        self.title = "Encomendas - J & N Artefatos de Cimento"

        # Session to use in all functionalities of the app.
        self.session = get_session()

        # Add an easy reference on the app to all main screens except menu to
        # later use.
        self.new_order = NewOrder(name='new_order')
        self.consult = Consult(name="consult")
        self.payments = Payments(name="payments")
        self.orders = Orders(name="orders")
        self.prices = Prices(name="prices")

        # Create the main screen manager and add an easy reference on the app.
        self.sm = ScreenManager(transition=SwapTransition())

        # Add all the screens to the manager
        self.sm.add_widget(Menu(name="menu"))
        self.sm.add_widget(self.new_order)
        self.sm.add_widget(self.consult)
        self.sm.add_widget(self.payments)
        self.sm.add_widget(self.orders)
        self.sm.add_widget(self.prices)

        # Return the root widget.
        return self.sm


if __name__ == '__main__':
    JnApp().run()
