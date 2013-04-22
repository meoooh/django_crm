# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('crm_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], to_field='username', unique=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('lastIp', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal('crm', ['UserProfile'])

        # Adding model 'WorkDailyRecord'
        db.create_table('crm_workdailyrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], to_field='username')),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('ongoing_or_end', self.gf('django.db.models.fields.CharField')(default='ing', max_length=3)),
        ))
        db.send_create_signal('crm', ['WorkDailyRecord'])

        # Adding M2M table for field check_user on 'WorkDailyRecord'
        db.create_table('crm_workdailyrecord_check_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workdailyrecord', models.ForeignKey(orm['crm.workdailyrecord'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('crm_workdailyrecord_check_user', ['workdailyrecord_id', 'user_id'])

        # Adding M2M table for field target_user on 'WorkDailyRecord'
        db.create_table('crm_workdailyrecord_target_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workdailyrecord', models.ForeignKey(orm['crm.workdailyrecord'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('crm_workdailyrecord_target_user', ['workdailyrecord_id', 'user_id'])

        # Adding model 'Note'
        db.create_table('crm_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], to_field='username')),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('crm', ['Note'])

        # Adding model 'IPaddr'
        db.create_table('crm_ipaddr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('addr', self.gf('django.db.models.fields.GenericIPAddressField')(unique=True, max_length=39)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('crm', ['IPaddr'])

        # Adding model 'PersonInCharge'
        db.create_table('crm_personincharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telephone1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('telephone2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('mobile1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('mobile2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('email1', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('email2', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
        ))
        db.send_create_signal('crm', ['PersonInCharge'])

        # Adding model 'Domain'
        db.create_table('crm_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('crm', ['Domain'])

        # Adding model 'Equipment'
        db.create_table('crm_equipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='etc', max_length=4, null=True)),
            ('ipaddr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.IPaddr'], to_field='addr')),
        ))
        db.send_create_signal('crm', ['Equipment'])

        # Adding model 'Customer'
        db.create_table('crm_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('serviceName', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('detailedServiceName', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('serviceNumber', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('dataFolder', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('crm', ['Customer'])

        # Adding M2M table for field personInCharges on 'Customer'
        db.create_table('crm_customer_personInCharges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('personincharge', models.ForeignKey(orm['crm.personincharge'], null=False))
        ))
        db.create_unique('crm_customer_personInCharges', ['customer_id', 'personincharge_id'])

        # Adding M2M table for field workers on 'Customer'
        db.create_table('crm_customer_workers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('crm_customer_workers', ['customer_id', 'user_id'])

        # Adding M2M table for field salespersons on 'Customer'
        db.create_table('crm_customer_salespersons', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('crm_customer_salespersons', ['customer_id', 'user_id'])

        # Adding M2M table for field ipaddrs on 'Customer'
        db.create_table('crm_customer_ipaddrs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('ipaddr', models.ForeignKey(orm['crm.ipaddr'], null=False))
        ))
        db.create_unique('crm_customer_ipaddrs', ['customer_id', 'ipaddr_id'])

        # Adding M2M table for field domains on 'Customer'
        db.create_table('crm_customer_domains', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('domain', models.ForeignKey(orm['crm.domain'], null=False))
        ))
        db.create_unique('crm_customer_domains', ['customer_id', 'domain_id'])

        # Adding M2M table for field equipments on 'Customer'
        db.create_table('crm_customer_equipments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('equipment', models.ForeignKey(orm['crm.equipment'], null=False))
        ))
        db.create_unique('crm_customer_equipments', ['customer_id', 'equipment_id'])

        # Adding M2M table for field alertEmails on 'Customer'
        db.create_table('crm_customer_alertEmails', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('personincharge', models.ForeignKey(orm['crm.personincharge'], null=False))
        ))
        db.create_unique('crm_customer_alertEmails', ['customer_id', 'personincharge_id'])

        # Adding M2M table for field alertSMSs on 'Customer'
        db.create_table('crm_customer_alertSMSs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('personincharge', models.ForeignKey(orm['crm.personincharge'], null=False))
        ))
        db.create_unique('crm_customer_alertSMSs', ['customer_id', 'personincharge_id'])

        # Adding model 'ResponsingAttackDetection'
        db.create_table('crm_responsingattackdetection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='Defacement', max_length=2, null=True, blank=True)),
            ('attackerIp', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ResponsingAttackDetection_attackerIp_set', to=orm['crm.IPaddr'])),
            ('victimIp', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ResponsingAttackDetection_victimIp_set', null=True, to=orm['crm.IPaddr'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], to_field='username')),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Customer'], to_field='name')),
            ('emailRecipient', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('smsRecipient', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('crm', ['ResponsingAttackDetection'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('crm_userprofile')

        # Deleting model 'WorkDailyRecord'
        db.delete_table('crm_workdailyrecord')

        # Removing M2M table for field check_user on 'WorkDailyRecord'
        db.delete_table('crm_workdailyrecord_check_user')

        # Removing M2M table for field target_user on 'WorkDailyRecord'
        db.delete_table('crm_workdailyrecord_target_user')

        # Deleting model 'Note'
        db.delete_table('crm_note')

        # Deleting model 'IPaddr'
        db.delete_table('crm_ipaddr')

        # Deleting model 'PersonInCharge'
        db.delete_table('crm_personincharge')

        # Deleting model 'Domain'
        db.delete_table('crm_domain')

        # Deleting model 'Equipment'
        db.delete_table('crm_equipment')

        # Deleting model 'Customer'
        db.delete_table('crm_customer')

        # Removing M2M table for field personInCharges on 'Customer'
        db.delete_table('crm_customer_personInCharges')

        # Removing M2M table for field workers on 'Customer'
        db.delete_table('crm_customer_workers')

        # Removing M2M table for field salespersons on 'Customer'
        db.delete_table('crm_customer_salespersons')

        # Removing M2M table for field ipaddrs on 'Customer'
        db.delete_table('crm_customer_ipaddrs')

        # Removing M2M table for field domains on 'Customer'
        db.delete_table('crm_customer_domains')

        # Removing M2M table for field equipments on 'Customer'
        db.delete_table('crm_customer_equipments')

        # Removing M2M table for field alertEmails on 'Customer'
        db.delete_table('crm_customer_alertEmails')

        # Removing M2M table for field alertSMSs on 'Customer'
        db.delete_table('crm_customer_alertSMSs')

        # Deleting model 'ResponsingAttackDetection'
        db.delete_table('crm_responsingattackdetection')


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
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'crm.equipment': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Equipment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.IPaddr']", 'to_field': "'addr'"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'etc'", 'max_length': '4', 'null': 'True'})
        },
        'crm.ipaddr': {
            'Meta': {'ordering': "['addr']", 'object_name': 'IPaddr'},
            'addr': ('django.db.models.fields.GenericIPAddressField', [], {'unique': 'True', 'max_length': '39'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crm.note': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Note'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"})
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
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'smsRecipient': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'to_field': "'username'"}),
            'victimIp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ResponsingAttackDetection_victimIp_set'", 'null': 'True', 'to': "orm['crm.IPaddr']"})
        },
        'crm.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastIp': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
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