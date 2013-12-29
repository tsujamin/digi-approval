# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workflow'
        db.create_table(u'digiapproval_workflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_customer', to=orm['auth.User'])),
            ('approver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_approver', to=orm['auth.User'])),
            ('workflow', self.gf('digiapproval_project.apps.digiapproval.fields.WorkflowField')()),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digiapproval.WorkflowSpec'])),
        ))
        db.send_create_signal(u'digiapproval', ['Workflow'])

        # Adding model 'WorkflowSpec'
        db.create_table(u'digiapproval_workflowspec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='64')),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spec', self.gf('digiapproval_project.apps.digiapproval.fields.WorkflowSpecField')()),
        ))
        db.send_create_signal(u'digiapproval', ['WorkflowSpec'])


    def backwards(self, orm):
        # Deleting model 'Workflow'
        db.delete_table(u'digiapproval_workflow')

        # Deleting model 'WorkflowSpec'
        db.delete_table(u'digiapproval_workflowspec')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'digiapproval.userfile': {
            'Meta': {'object_name': 'UserFile'},
            '_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'virus_status': ('django.db.models.fields.CharField', [], {'default': "'UNSCANNED'", 'max_length': '16'})
        },
        u'digiapproval.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_approver'", 'to': u"orm['auth.User']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_customer'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digiapproval.WorkflowSpec']"}),
            'workflow': ('digiapproval_project.apps.digiapproval.fields.WorkflowField', [], {})
        },
        u'digiapproval.workflowspec': {
            'Meta': {'object_name': 'WorkflowSpec'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'64'"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spec': ('digiapproval_project.apps.digiapproval.fields.WorkflowSpecField', [], {})
        }
    }

    complete_apps = ['digiapproval']