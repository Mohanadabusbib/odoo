# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TestApp(models.Model):
    _name = 'my.app'
    _description = 'Hello World'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='My Name',required=True, tracking=True)
    value = fields.Integer(default=36)
    value2 = fields.Float()
    description = fields.Text(default='enter the Description')
    trueFalse = fields.Boolean()
    html = fields.Html()
    date = fields.Date()
    datetime = fields.Datetime()
    binary = fields.Binary()
    selection = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C')],default='A')
    col1 = fields.Float(string='Val 01')
    col2 = fields.Float(string='Val 02')
    result = fields.Float(string="Result",readonly=True)
    computed = fields.Float(readonly=True,compute='_value_pc',store=True)
    state = fields.Selection([('new','New'),('reviewed', 'Reviewed'), ('approved', 'Approved'),('rejected', 'Rejected')], default='new')

    _sql_constraints = [
        ('uniq_name','unique(name)', 'The name must be unique.')
    ]

    @api.constrains('value')
    def _check_age(self):
        if self.value <= 25 or self.value >= 35:
            raise  ValidationError(_('You must be between 25 and 35 years old.'))

    @api.onchange('col1','col2')
    def on_change_val(self):
        self.result = self.col1 + self.col2
        

    @api.depends('result')
    def _value_pc(self):
        for record in self:
            record.computed = float(record.result) / 100

    def event_reviewed(self):
        self.state = 'reviewed'

    def event_approved(self):
        self.state = 'approved'

    def event_rejected(self):
        self.state = 'rejected'