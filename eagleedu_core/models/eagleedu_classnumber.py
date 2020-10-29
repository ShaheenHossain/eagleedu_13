# -*- coding: utf-8 -*-

from eagle.exceptions import ValidationError
from eagle import fields, models, api, _


class EagleeduClassnumber(models.Model):
    _name = 'eagleedu.classnumber'
    _description = "Class Room Number"

    name = fields.Integer(string='Class Room Number', help="Enter the Room Number of the Class")

    classnumber_ids = fields.Many2many('eagleedu.classnumber', 'eagleedu_classnumber_rel', 'classnumber_ids')


