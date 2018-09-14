from db import Client, Order
from kivy.app import App
from kivy.uix.screenmanager import Screen
from sqlalchemy import not_

class OrderList(Screen):
    """Screen that show all the orders to select for editing."""

    def filter(self):
        """Filter the orders."""
        # Get the informations.
        search_query = self.ids['search'].text.strip()
        show_delivered = self.ids['show_delivered'].state == 'down'

        # Get query from app session and filter by id.
        app = App.get_running_app()
        query = app.session.query(Order, Client)
        query = query.filter(Client.id == Order.client_id)

        # Filter from informations.
        if search_query:
            query = query.filter(Client.name.ilike(f"%{search_query}%"))
        if not show_delivered:
            query = query.filter(not_(Order.delivered))

        # Parse and update RecycleView orders data.
        orders = [{
            'order_id':i[0].id,
            'client_name': i[1].name,
            'delivered': i[0].delivered,
            'local': i[0].local
        } for i in query.all()]
        self.ids['orders'].data = reversed(orders)

    def on_pre_enter(self):
        """Update informations before entering screen."""
        self.ids['search'].text = ''
        self.ids['show_delivered'].state = 'normal'
        self.ids['dont_show_delivered'].state = 'down'
        self.filter()

    def edit_order_info(self, order_id):
        """Go to screen to edit order info."""
        self.manager.order_id = order_id
        self.manager.current = 'edit'
