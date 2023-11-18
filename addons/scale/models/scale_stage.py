from odoo import api, fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

class Stage(models.Model):
    """ Modelo para las etapas del proceso de un camion
    """
    _name = "scale.stage"
    _description = "Etapas de un camión"
    _rec_name = 'name'
    #_order = "sequence, name, id"

    name = fields.Char('Nombre etapa', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    active = fields.Boolean(default=True)
    unattended = fields.Boolean(string="Unattended")
    closed = fields.Boolean(string="Closed")
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")
    #team_id = fields.Many2one('crm.team', string='Sales Team', ondelete='set null',
    #    help='Specific team that uses this stage. Other teams will not be able to see or use this stage.')
    fold = fields.Boolean(
        string="Folded in Kanban",
        help="This stage is folded in the kanban view "
        "when there are no records in that stage "
        "to display.",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )