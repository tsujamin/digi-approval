# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserFile'
        db.create_table(u'digiapproval_userfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('viruschecked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'digiapproval', ['UserFile'])


    def backwards(self, orm):
        # Deleting model 'UserFile'
        db.delete_table(u'digiapproval_userfile')


    models = {
        u'digiapproval.userfile': {
            'Meta': {'object_name': 'UserFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'viruschecked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['digiapproval']