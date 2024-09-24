from odoo import models, fields, api

class MyOrder(models.Model):
    _name = 'my.order'
    _description = 'My Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    datetime = fields.Datetime()
    items_ids = fields.One2many('my.order.items', 'order_id')
    state = fields.Selection([('new','New'),('ready', 'Ready')], default='new')
    isActive = fields.Boolean(default=True)
    

    def event_ready(self):
        self.state = 'ready'
    
    def add_item(self):
        self.env['my.order.items'].create({
            'name': 'test',
            'itemPrice': 200,
            'qty': 1,
            'order_id': self.id
        })

    def get_query(self):
        query_rst = self.env['my.order.items'].search([('qty', '>', 1)])
        for item in query_rst:
            print(item.name)
            

class MyOrdersItems(models.Model):
    _name = 'my.order.items'
    _description = 'My Order Items'

    name = fields.Char()
    itemPrice = fields.Float()
    qty = fields.Integer()
    order_id = fields.Many2one('my.order',domain="[('state', '=', 'ready'),('isActive', '=', True)]")