from odoo import fields, models
import threading
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class Scale(models.Model):
    _name = "scale"
    _description = "Scale cosas"

    #el numero del ticket = NombreBalanza + secuencia
    name = fields.Char(string="Nombre medición",index=True, required=True,readonly=True)

    scale_name = fields.Char(string="Nombre balanza")   #TODO: que sea una fk a un objecto scale.type
    observations = fields.models.CharField(string="Observaciones", max_length=420)
    weight_gross = fields.Float(string="Peso bruto")
    weight_tare  = fields.Float(string="Peso tara")
    weight_net   = fields.Float(string="Peso neto")

    create_date = fields.Datetime(string="Fecha de creación")
    weight_gross_date = fields.Datetime(string="Fecha de pesaje neto")
    weight_tare_date = fields.Datetime(string="Fecha de pesaje tara")
    gitHub_closed_date = fields.Datetime(string="Fecha de cierre en GitHub")

    isGoinIn = fields.models.BooleanField(string="Entrada", default=True)
    isGross = fields.models.BooleanField(string="Neto", default=False)
    measurement_number = fields.models.models.IntegerField(string="Pesada", default=1) #1 medida inicial, 2 medida final
    #TODO: deberia guardar las patentes en el chofer, tambien cada chofer 
    # deberia tener una lista de posibles patente a elegir para cada una
    licence_plate_chasis = fields.Char(string="Patente Chasis")
    licence_plate_trailer = fields.Char(string="Patente Acoplado")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Empresa",
        required=True,
        default=lambda self: self.env.company,
    )
    user_id = fields.Many2one(
        comodel_name="res.users", 
        string="Operador", 
        tracking=True, 
        index=True
        #domain="team_id"
    )
    carrier_id = fields.Many2one(
        comodel_name="res.company",
        string="Transportista",
        required=False,
    )
    choffer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Conductor"
    )
    product_id = fields.Many2one("product.product", string="Producto")
    product_description = fields.models.CharField(string="Descripción", max_length=50)
    
    #estos tambien deberian ser partners pero por ahora los dejamos asi
    sender = fields.models.CharField(string="remitente", max_length=50)
    sender_cuit = fields.models.CharField(string="CUIT remitente", max_length=11)
    reciever = fields.models.CharField(string="Destinatario", max_length=50)
    reciever_cuit = fields.models.CharField(string="CUIT destinatario", max_length=11)

    product_description = fields.models.CharField(string="Descripción", max_length=50)
    product_description = fields.models.CharField(string="Descripción", max_length=50)

    stage_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict')
        #domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]") #todo agregar grupos

    kanban_state = fields.Selection([
        ('grey', 'No next activity planned'),
        ('red', 'Next activity late'),
        ('green', 'Next activity is planned')], string='Kanban State')
        #compute='_compute_kanban_state')

    # ---------------------------------------------------
    # CRUD
    # ---------------------------------------------------

    #TODO, primero hay que crear la secuencia
    #@api.model
    #def create(self, vals):
    #    if vals.get("pes", "/") == "/":
    #        vals["pes"] = self._prepare_ticket_number(vals)
    #    return super().create(vals)
    #
    #def _prepare_measurement(self, values):
    #    seq = self.env["ir.sequence"]
    #    if "company_id" in values:
    #        seq = seq.with_context(force_company=values["company_id"])
    #    return seq.next_by_code("scale.sequence") or "/"

    #TODO
    #def copy(self, default=None):
    #    self.ensure_one()
    #    if default is None:
    #        default = {}
    #    if "pes" not in default:
    #        default["pes"] = self._prepare_ticket_number(default)
    #    res = super().copy(default)
    #    return res
#
    #def write(self, vals):
    #    for _ticket in self:
    #        now = fields.Datetime.now()
    #        if vals.get("stage_id"):
    #            stage = self.env["helpdesk.ticket.stage"].browse([vals["stage_id"]])
    #            vals["last_stage_update"] = now
    #            if stage.closed:
    #                vals["closed_date"] = now
    #        if vals.get("user_id"):
    #            vals["assigned_date"] = now
    #    return super().write(vals)

    #@api.depends('activity_date_deadline')
    #def _compute_kanban_state(self):
    #    today = date.today()
    #    for lead in self:
    #        kanban_state = 'grey'
    #        if lead.activity_date_deadline:
    #            lead_date = fields.Date.from_string(lead.activity_date_deadline)
    #            if lead_date >= today:
    #                kanban_state = 'green'
    #            else:
    #                kanban_state = 'red'
    #        lead.kanban_state = kanban_state