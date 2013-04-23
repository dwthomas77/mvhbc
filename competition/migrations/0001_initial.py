# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('competition_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street_1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('street_2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('competition', ['Address'])

        # Adding model 'BrewerProfile'
        db.create_table('competition_brewerprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Address'], unique=True)),
            ('phone_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('entries_paid', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('insert_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('competition', ['BrewerProfile'])

        # Adding model 'Category'
        db.create_table('competition_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_id', self.gf('django.db.models.fields.IntegerField')()),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category_type', self.gf('django.db.models.fields.CharField')(default='Lager', max_length=200)),
        ))
        db.send_create_signal('competition', ['Category'])

        # Adding model 'Style'
        db.create_table('competition_style', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Category'])),
            ('style_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('style_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('competition', ['Style'])

        # Adding model 'Submission'
        db.create_table('competition_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.BrewerProfile'])),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Style'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('competition', ['Submission'])

        # Adding model 'Judge'
        db.create_table('competition_judge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('club_affiliation', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('judge_pref', self.gf('django.db.models.fields.CharField')(default='Judge', max_length=100)),
            ('qualification', self.gf('django.db.models.fields.CharField')(default='AP', max_length=3)),
            ('bjcp_registration', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('competition', ['Judge'])

        # Adding M2M table for field cat_pref_yes on 'Judge'
        db.create_table('competition_judge_cat_pref_yes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('judge', models.ForeignKey(orm['competition.judge'], null=False)),
            ('category', models.ForeignKey(orm['competition.category'], null=False))
        ))
        db.create_unique('competition_judge_cat_pref_yes', ['judge_id', 'category_id'])

        # Adding M2M table for field cat_pref_no on 'Judge'
        db.create_table('competition_judge_cat_pref_no', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('judge', models.ForeignKey(orm['competition.judge'], null=False)),
            ('category', models.ForeignKey(orm['competition.category'], null=False))
        ))
        db.create_unique('competition_judge_cat_pref_no', ['judge_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('competition_address')

        # Deleting model 'BrewerProfile'
        db.delete_table('competition_brewerprofile')

        # Deleting model 'Category'
        db.delete_table('competition_category')

        # Deleting model 'Style'
        db.delete_table('competition_style')

        # Deleting model 'Submission'
        db.delete_table('competition_submission')

        # Deleting model 'Judge'
        db.delete_table('competition_judge')

        # Removing M2M table for field cat_pref_yes on 'Judge'
        db.delete_table('competition_judge_cat_pref_yes')

        # Removing M2M table for field cat_pref_no on 'Judge'
        db.delete_table('competition_judge_cat_pref_no')


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
        'competition.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'street_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'competition.brewerprofile': {
            'Meta': {'object_name': 'BrewerProfile'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Address']", 'unique': 'True'}),
            'entries_paid': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'competition.category': {
            'Meta': {'ordering': "['category_id']", 'object_name': 'Category'},
            'category_id': ('django.db.models.fields.IntegerField', [], {}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category_type': ('django.db.models.fields.CharField', [], {'default': "'Lager'", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'competition.judge': {
            'Meta': {'object_name': 'Judge'},
            'bjcp_registration': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cat_pref_no': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'no+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['competition.Category']"}),
            'cat_pref_yes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'yes+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['competition.Category']"}),
            'club_affiliation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judge_pref': ('django.db.models.fields.CharField', [], {'default': "'Judge'", 'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'qualification': ('django.db.models.fields.CharField', [], {'default': "'AP'", 'max_length': '3'})
        },
        'competition.style': {
            'Meta': {'object_name': 'Style'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'style_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'style_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'competition.submission': {
            'Meta': {'object_name': 'Submission'},
            'brewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.BrewerProfile']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Style']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['competition']