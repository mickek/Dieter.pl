# -*- coding: utf-8 -*-    

from south.db import db
from django.db import models
from dieter.patients.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Profile.practice'
        db.add_column('patients_profile', 'practice', orm['patients.profile:practice'])
        
        # Changing field 'UserData.date'
        # (to signature: django.db.models.fields.DateField(default=datetime.datetime(2009, 10, 4, 23, 48, 38, 995590)))
        db.alter_column('patients_userdata', 'date', orm['patients.userdata:date'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Profile.practice'
        db.delete_column('patients_profile', 'practice_id')
        
        # Changing field 'UserData.date'
        # (to signature: django.db.models.fields.DateField(auto_now=True, blank=True))
        db.alter_column('patients_userdata', 'date', orm['patients.userdata:date'])
        
    
    
    models = {
        'patients.coupon': {
            'coupon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 4, 23, 48, 39, 272991)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 4, 23, 48, 39, 272877)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'patients.profile': {
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutritionist.PrivatePractice']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'target_weight': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'patients.userdata': {
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2009, 10, 4, 23, 48, 39, 75297)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'waist': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'nutritionist.privatepractice': {
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'nip': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'registration_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'regon': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['patients']
