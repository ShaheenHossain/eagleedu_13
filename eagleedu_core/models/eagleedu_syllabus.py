# -*- coding: utf-8 -*-

from eagle.exceptions import ValidationError
from eagle import fields, models, api, _


class EagleeduSyllabus(models.Model):
    _name = 'eagleedu.syllabus'
    _description = "Syllabus "
    _rec_name='display'
    _order = 'sequence'


    name = fields.Char(string='Name', help="Enter the Name of the Syllabus")
    # syllabus_code = fields.Char(string='Syllabus Code', compute="_get_code")
    display=fields.Char('Syllabus Display',help="This is printed on the marksheet as Subject")
    class_id = fields.Many2one('eagleedu.class', string='Class ID')
    subject_id = fields.Many2one('eagleedu.subject', string='Subject', copy=False)
    academic_year = fields.Many2one('eagleedu.academic.year', string='Academic Year')
    code = fields.Char('Code', compute="_get_code")
    sequence = fields.Integer(default=0, help="Gives the sequence order when displaying a list.")

    #for copy all the value as product template
    # attribute_line_ids = fields.One2many('eagleedu.syllabus', 'class_id', copy=True)

    # has_group=fields.Integer(related='class_id.division_count')
    divisional=fields.Boolean("Grouping ?")
    division_id = fields.Many2one('eagleedu.group_division', string='Group')

    paper = fields.Char( string='Paper')
    active=fields.Boolean('Active?',related='academic_year.active')
    compulsory_for=fields.Many2many('eagleedu.class.history','eagleedu_syllabus_class_history_rel',
                                    'compulsory_for','compulsory_subjects','compulsory for')
    selective_for=fields.Many2many('eagleedu.class.history','eagleedu_syllabus_class_history_1_rel',
                                    'selective_for','selective_subjects','selective for')
    optional_for=fields.Many2many('eagleedu.class.history','eagleedu_syllabus_class_history_optional_rel',
                                    'optional_for','optional_subjects','Optional for')

    subject_type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Subject Type', default="theory", required=True)
    selection_type = fields.Selection(
        [('compulsory', 'Compulsory'), ('elective', 'Elective')],
        'Selection Type', default="compulsory", required=True)
    evaluation_type = fields.Selection(
        [('general', 'General'),('extra','Extra')],
        'Evaluation Type', default="general", required=True)

    # total_hours = fields.Float(string='Total Hours')
    total_mark=fields.Integer('Total')
    pass_mark=fields.Integer('Pass')
    tut_mark=fields.Integer('Tutorial')
    tut_pass=fields.Integer('pass')
    subj_mark = fields.Integer('Subjective')
    subj_pass = fields.Integer('pass')
    obj_mark = fields.Integer('Objective')
    obj_pass = fields.Integer('pass')
    prac_mark = fields.Integer('Practical')
    prac_pass = fields.Integer('pass')
    description = fields.Text(string='Syllabus Modules')

    @api.onchange('academic_year','class_id','division_id','subject_id','paper')
    def _get_code(self):
        for rec in self:
            recname=''
            reccode=''
            if rec.paper and rec.subject_id:
                recname=rec.subject_id.name +'-'+ rec.paper
                reccode=rec.subject_id.code +'-'+ rec.paper
            elif rec.subject_id:
                recname=rec.subject_id.name
                reccode=rec.subject_id.code
            rec.display = recname
            if recname != '':
                if  rec.class_id :
                    if rec.academic_year :
                        if rec.divisional == True:
                            recname=recname +'-'+ rec.class_id.name +'-' + rec.academic_year.name # +' ('+rec.division_id.name +')'
                            reccode=reccode +'-'+ rec.class_id.code +'-' + rec.academic_year.ay_code # +' ('+rec.division_id.code +')'
                        else:
                            recname = recname +'-'+ rec.class_id.name + '-' + rec.academic_year.name
                            reccode = reccode +'-'+ rec.class_id.code + '-' + rec.academic_year.ay_code
                            rec.division_id=False
            rec.name=recname
            rec.code=reccode
    @api.model
    @api.onchange('tut_mark','subj_mark','obj_mark','prac_mark','tut_pass','subj_pass','obj_pass','prac_pass')
    def calculate_total_mark(self):
        for rec in self:
            rec.total_mark=rec.tut_mark+rec.subj_mark+rec.obj_mark+rec.prac_mark
            rec.pass_mark=rec.tut_pass+rec.subj_pass+rec.obj_pass+rec.prac_pass

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     # TDE FIXME: should probably be copy_data
    #     self.ensure_one()
    #     if default is None:
    #         default = {}
    #     if 'subject_id' not in default:
    #         default['subject_id'] = _("%s (copy)") % self.subject_id
    #     return super(EagleeduSyllabus, self).copy(default=default)

#disabled the sql constrain

    # _sql_constraints = [('unque_syllabus_batch_level','unique(subject_id,academic_year,division_id,class_id,paper)','Subject Already added!'),]

    # attribute_line_ids = fields.One2many('product.template.attribute.line', 'product_tmpl_id', 'Product Attributes', copy=True)

