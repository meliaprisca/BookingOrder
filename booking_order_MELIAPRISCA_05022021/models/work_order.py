from odoo import models, fields, api, _

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Model Work Order'

    name = fields.Char(string='WO Number', readonly=True, copy=False, default=lambda self: _('New'))
    booking_order_ref = fields.Many2one('sale.order', string='Booking Order Reference', required=True,)
    # partner_id = fields.Many2one('res.partner', string='Customer', required=True,)
    team_id = fields.Many2one('service.team', string='Team', required=True, )
    leader_id = fields.Many2one('res.users', string='Team Leader', required=True, )
    member_id = fields.Many2many('res.users', string='Team Members')
    plan_start = fields.Datetime(string='Planned Start', required=True, )
    plan_end = fields.Datetime(string='Planned End', required=True, )
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
            ('pending','Pending'),
            ('pro','In Progress'),
            ('done','Done'), 
            ('cancel','Cancelled'),], 
            string='State',
            default='pending')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('wo.sequence')
        return super().create(vals)
    
    def action_pending(self):
        self.write({'state': 'pending'})

    @api.onchange('booking_order_ref')
    def get_book_order(self):
        # self.partner_id = self.booking_order_ref.partner_id
        self.team_id = self.booking_order_ref.team
        self.leader_id = self.booking_order_ref.leader_id
        self.member_id = self.booking_order_ref.member_id
        self.plan_start = self.booking_order_ref.book_start
        self.plan_end = self.booking_order_ref.book_end

    def action_pro(self):
        for rec in self:
            rec.date_start = fields.datetime.now()
            rec.state = 'pro'
    
    def action_done(self):
        for rec in self:
            rec.date_end = fields.datetime.now()
            rec.state = 'done'

    def action_cancel(self):
        res = self.env.ref('booking_order_MELIAPRISCA_05022021.cancel_state_wizard_action')
        return res.read()[0]