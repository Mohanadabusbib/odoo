# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class Patients(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string="Is Patient")
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(string="Age")
    app_count = fields.Integer(string="Count", compute="get_app_count")
    

    def get_appointment(self):
        action = {
            'name': 'appointments',
            'res_model': 'the.appointments',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.id)]
        }
        return action
        
    def get_app_count(self):
        self.app_count = self.env['the.appointments'].search_count([('patient_id', '=', self.id)])
        

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_doctor = fields.Boolean(string='Is Doctor')
    is_supervisor = fields.Boolean(string="Is Supervisor")
    appointment_ids = fields.One2many("the.appointments", "doctor_id")


class TheAppointments(models.Model):
    _name = "the.appointments"
    _description = 'Appointments module'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Appointment Id', required=True, copy=False, readonly=True,
                index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('res.partner', string='Patient', required=True,
                domain="[('is_patient', '=', True)]")
    patient_age = fields.Integer(string='Age', related='patient_id.age')
    notes = fields.Text(string='notes')
    app_date = fields.Datetime(string="Date Time", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],string='Status',readonly=True, default='draft',
    )
    doctor_notes = fields.Text(string="Doctor Notes")
    prescription_ids = fields.One2many('the.prescription', 'appointment_id')
    doctor_id = fields.Many2one('res.users', string="Doctor",domain="[('is_doctor', '=', True)]")   
    

    def action_confirm(self):
        for item in self:
            item.state = 'confirmed'
    

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('the.appointments.sequence') or _('New')
        result = super(TheAppointments, self).create(vals)
        return result
    
    def changdate(self):
        for item in self:
            if item.app_date < datetime.today():
                item.state = 'cancel'
            

    def action_cconfirm(self):
        for item in self:
            item.state = 'confirmed'
    def action_done(self):
        for item in self:
            item.state = 'done'
    
    def action_cancel(self):
        for item in self:
            item.state = 'cancel'

class Prescription(models.Model):
    _name = "the.prescription"

    name = fields.Char(string="Medic Name")
    notes = fields.Text(string="Notes")
    appointment_id = fields.Many2one('the.appointments', string="Appointment")
    medicines_id = fields.Many2one('the.medicines', string="Medicine")

class Medicines(models.Model):
    _name = "the.medicines"

    name = fields.Char(string="Medic Name")
    effective_material = fields.Text(string="Effective Material")
    prescription_ids = fields.One2many('the.prescription', 'medicines_id')