# -*- coding: utf-8 -*-

from eagle import fields, models, api, _
from eagle.exceptions import ValidationError
from datetime import date,datetime

class importAllStudent(models.Model):
    _name='eagleedu.import.previous.student'
    name=fields.Char('Name')

    # @api.model
    # def _get_groups(self):
    #     lst = []
    #
    #     for record in self:
    #         groups = self.env['eagleedu.application'].search([('register_id.id', '=', record.register_id.id)])
    #         for group in groups:
    #             lst.append((group.id, group.name))
    #     return lst
    date=fields.Date(default=fields.Date.today)
    import_qty=fields.Integer('No of Student to Import')
    register_id=fields.Many2one('eagleedu.register',"Import student Of")
    level=fields.Integer(related='register_id.standard.id')
    import_group=fields.Char('From Group')
    import_section=fields.Char(string="section")#([('a','A'),('b','B'),('c','C'),('d','D')],'From Section')
    assign_class=fields.Many2one('eagleedu.class.division',"Assign Student to")
    students_to_assign=fields.One2many('eagleedu.application','import_id',"Student List")
    # state=fields.Selection([(1,'draft'),(2,'done')],default='1')

        # @api.onchange('import_standard')
    # def get_student_to_import(self):
    #     for rec in self:
    #         if self.import_standard:
    #             applications=self.env['eagleedu.application'].search([('register_id.standard','=',self.import_standard)])
    #             if self.student_to_assign:
    #                 applications=self.env['eagleedu.application'].search([register_id('section','=',self.section),('group','=',self.group)])
    #



    #@api.multi
    def import_students(self):
        lst = [('register_id', '=', self.register_id.id)]


        if self.import_section:
            lst.append(('section', '=', self.import_section))
        if self.import_group:
            lst.append(('group','=',self.import_group))

        applications=self.env['eagleedu.application'].search(lst,order='id asc')
        for app in applications:
            if app.student_id:
                # verify student
                #document_ids = self.env['eagleedu.documents'].search([('application_ref', '=', app.id)])
                # if not document_ids:
                #     raise ValidationError(_('No Documents provided'))
                app.write({
                    'state': 'verification'
                })
                # insert documents
                doc_details={ 'application_ref': app.id,
                              # 'document_name':1,
                              'has_hard_copy':False,
                              'reference':1
                              }
                documents=self.env['eagleedu.documents']
                documentedu=documents.create(doc_details)
                documentedu.write({
                    'verified_by': self.env.uid,
                    'verified_date': datetime.now().strftime("%Y-%m-%d"),
                    'state': 'done'
                })
                app.write({
                    'verified_by': self.env.uid,
                    'state': 'approve',
                    'class_id': self.assign_class.id,
                    'import_id': self.id
                })
                student=app.create_student()

