# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomerAccount'
        db.create_table(u'digiapproval_customeraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('account_type', self.gf('django.db.models.fields.CharField')(default='CUSTOMER', max_length=16)),
        ))
        db.send_create_signal(u'digiapproval', ['CustomerAccount'])

        # Adding M2M table for field related_accounts on 'CustomerAccount'
        m2m_table_name = db.shorten_name(u'digiapproval_customeraccount_related_accounts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_customeraccount', models.ForeignKey(orm[u'digiapproval.customeraccount'], null=False)),
            ('to_customeraccount', models.ForeignKey(orm[u'digiapproval.customeraccount'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_customeraccount_id', 'to_customeraccount_id'])


        # Changing field 'Workflow.customer'
        db.alter_column(u'digiapproval_workflow', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digiapproval.CustomerAccount']))

    def backwards(self, orm):
        # Deleting model 'CustomerAccount'
        db.delete_table(u'digiapproval_customeraccount')

        # Removing M2M table for field related_accounts on 'CustomerAccount'
        db.delete_table(db.shorten_name(u'digiapproval_customeraccount_related_accounts'))


        # Changing field 'Workflow.customer'
        db.alter_column(u'digiapproval_workflow', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

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
            'related_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['digiapproval.CustomerAccount']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
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
            'spec': ('digiapproval_project.apps.digiapproval.fields.WorkflowSpecField', [], {})
        }
    }

    complete_apps = ['digiapproval']