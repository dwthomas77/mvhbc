# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Submission.submitted_on'
        db.add_column('competition_submission', 'submitted_on',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.datetime(2013, 2, 24, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Submission.received_on'
        db.add_column('competition_submission', 'received_on',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Submission.checked_in'
        db.add_column('competition_submission', 'checked_in',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Submission.submitted_on'
        db.delete_column('competition_submission', 'submitted_on')

        # Deleting field 'Submission.received_on'
        db.delete_column('competition_submission', 'received_on')

        # Deleting field 'Submission.checked_in'
        db.delete_column('competition_submission', 'checked_in')


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
            'checked_in': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'received_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Style']"}),
            'submitted_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
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