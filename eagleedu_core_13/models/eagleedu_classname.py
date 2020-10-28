# -*- coding: utf-8 -*-

from eagle.exceptions import ValidationError
from eagle import fields, models, api, _


class EagleeduClassname(models.Model):
    _name = 'eagleedu.classname'
    _description = "Class Name"

    name = fields.Char(string='Class Name', help="Enter the Name of the Class")

    classname_ids = fields.Many2many('eagleedu.classname', 'eagleedu_classname_rel', 'classname_ids')


