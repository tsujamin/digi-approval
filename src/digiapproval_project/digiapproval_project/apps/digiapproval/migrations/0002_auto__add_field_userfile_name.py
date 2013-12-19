# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserFile.name'
        db.add_column(u'digiapproval_userfile', 'name',
                      self.gf('django.db.models.fields.CharField')(default='unnamed file', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserFile.name'
        db.delete_column(u'digiapproval_userfile', 'name')


    models = {
        u'digiapproval.userfile': {
            'Meta': {'object_name': 'UserFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'viruschecked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['digiapproval']