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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('virus_status', self.gf('django.db.models.fields.CharField')(default='UNSCANNED', max_length=16)),
        ))
        db.send_create_signal(u'digiapproval', ['UserFile'])


    def backwards(self, orm):
        # Deleting model 'UserFile'
        db.delete_table(u'digiapproval_userfile')


    models = {
        u'digiapproval.userfile': {
            'Meta': {'object_name': 'UserFile'},
            '_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'virus_status': ('django.db.models.fields.CharField', [], {'default': "'UNSCANNED'", 'max_length': '16'})
        }
    }

    complete_apps = ['digiapproval']