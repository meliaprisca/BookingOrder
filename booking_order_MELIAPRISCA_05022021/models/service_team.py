from odoo import models, fields, api

class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Model Service Team'

    name = fields.Char(string='Team Name', required=True, )
    leader_id = fields.Many2one('res.users', string='Team Leader', required=True, )
    member_id = fields.Many2many('res.users',string='Team Member')