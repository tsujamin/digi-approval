# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.uuid'
        db.alter_column(u'digiapproval_task', 'uuid', self.gf('django.db.models.fields.CharField')(max_length='36'))
        # Adding field 'WorkflowSpec.toplevel'
        db.add_column(u'digiapproval_workflowspec', 'toplevel',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Task.uuid'
        db.alter_column(u'digiapproval_task', 'uuid', self.gf('django.db.models.fields.CharField')(max_length='32'))
        # Deleting field 'WorkflowSpec.toplevel'
        db.delete_column(u'digiapproval_workflowspec', 'toplevel')


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
        u'digiapproval.customeraccount': {
            'Meta': {'object_name': 'CustomerAccount'},
            'account_type': ('django.db.models.fields.CharField', [], {'default': "'CUSTOMER'", 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sub_accounts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['digiapproval.CustomerAccount']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'digiapproval.task': {
            'Meta': {'object_name': 'Task'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('jsonfield.fields.JSONField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': "'36'"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digiapproval.Workflow']"})
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
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_customer'", 'to': u"orm['digiapproval.CustomerAccount']"}),
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
            'spec': ('digiapproval_project.apps.digiapproval.fields.WorkflowSpecField', [], {}),
            'toplevel': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['digiapproval']