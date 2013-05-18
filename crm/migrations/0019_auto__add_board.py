# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table('crm_board', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('write', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], to_field='username', unique=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('notImg', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['Board'])


    def backwards(self, orm):
        # Deleting model 'Board'
        db.delete_table('crm_board')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'crm.board': {
            'Meta': {'object_name': 'Board'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'notImg': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'write': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'to_field': "'username'", 'unique': 'True'})
        },
        'crm.chatmessage': {
            'Meta': {'ordering': "['pk']", 'object_name': 'ChatMessage'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.ChatRoom']"}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"})
        },
        'crm.chatroom': {
            'Meta': {'object_name': 'ChatRoom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participant': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'crm.customer': {
            'Meta': {'object_name': 'Customer'},
            'alertEmails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_alertEmails_personincharge_set'", 'null': 'True', 'to': "orm['crm.PersonInCharge']"}),
            'alertSMSs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_alertSMSs_personincharge_set'", 'null': 'True', 'to': "orm['crm.PersonInCharge']"}),
            'dataFolder': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detailedServiceName': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'domains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_domains_domain_set'", 'null': 'True', 'to': "orm['crm.Domain']"}),
            'equipments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_equipments_equipment_set'", 'null': 'True', 'to': "orm['crm.Equipment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddrs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_ipaddrs_ipaddr_set'", 'null': 'True', 'to': "orm['crm.IPaddr']"}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'personInCharges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_personincharges_personincharge_set'", 'null': 'True', 'to': "orm['crm.PersonInCharge']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'salespersons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_salespersons_user_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'serviceName': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'serviceNumber': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customer_workers_user_set'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'crm.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'crm.equipment': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Equipment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.IPaddr']", 'to_field': "'addr'"}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'etc'", 'max_length': '4', 'null': 'True'})
        },
        'crm.history': {
            'Meta': {'ordering': "['pk']", 'object_name': 'History'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"})
        },
        'crm.ipaddr': {
            'Meta': {'ordering': "['addr']", 'object_name': 'IPaddr'},
            'addr': ('django.db.models.fields.GenericIPAddressField', [], {'unique': 'True', 'max_length': '39'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'crm.personincharge': {
            'Meta': {'object_name': 'PersonInCharge'},
            'email1': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'mobile2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'crm.responsingattackdetection': {
            'Meta': {'object_name': 'ResponsingAttackDetection'},
            'attackerIp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ResponsingAttackDetection_attackerIp_set'", 'to': "orm['crm.IPaddr']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Customer']", 'to_field': "'name'"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'emailRecipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'Defacement'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'smsRecipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"}),
            'victimIp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ResponsingAttackDetection_victimIp_set'", 'null': 'True', 'to': "orm['crm.IPaddr']"})
        },
        'crm.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastIp': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'to_field': "'username'", 'unique': 'True'})
        },
        'crm.workdailyrecord': {
            'Meta': {'object_name': 'WorkDailyRecord'},
            'check_user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'checked_user_record_set'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ongoing_or_end': ('django.db.models.fields.CharField', [], {'default': "'ing'", 'max_length': '3'}),
            'target_user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'target_user_record_set'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"})
        }
    }

    complete_apps = ['crm']