import json
from decimal import Decimal

from kivy.uix.screenmanager import Screen

from util.brl import format_brl

class OrderDetails(Screen):
    """Screen to show the details of an order."""

    def on_pre_enter(self):
        """Update all information before entering."""
        order = self.manager.order
        itens = [{
            'name': iten['name'],
            'quantity': Decimal(iten['quantity']),
            'price': Decimal(iten['price'])
        } for iten in order.itens]
        self.ids['title'].text = f"Detalhes da encomenda número {order.id}."
        self.ids['delivered'].text = "Sim" if order.delivered else "Não"
        self.ids['local'].text = order.local
        self.ids['info'].text = order.extra_info
        self.ids['total'].text = format_brl(order.total)
        self.ids['itens'].data = itens
