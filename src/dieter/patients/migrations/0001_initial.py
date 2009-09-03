# -*- coding: utf-8 -*-    

from south.db import db
from django.db import models
from dieter.patients.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserData'
        db.create_table('patients_userdata', (
            ('date', orm['patients.UserData:date']),
            ('user', orm['patients.UserData:user']),
            ('id', orm['patients.UserData:id']),
            ('weight', orm['patients.UserData:weight']),
            ('waist', orm['patients.UserData:waist']),
        ))
        db.send_create_signal('patients', ['UserData'])
        
        # Adding model 'Coupon'
        db.create_table('patients_coupon', (
            ('coupon', orm['patients.Coupon:coupon']),
            ('id', orm['patients.Coupon:id']),
            ('user', orm['patients.Coupon:user']),
        ))
        db.send_create_signal('patients', ['Coupon'])
        
        # Adding model 'Profile'
        db.create_table('patients_profile', (
            ('target_weight', orm['patients.Profile:target_weight']),
            ('user', orm['patients.Profile:user']),
            ('height', orm['patients.Profile:height']),
            ('id', orm['patients.Profile:id']),
            ('sex', orm['patients.Profile:sex']),
        ))
        db.send_create_signal('patients', ['Profile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserData'
        db.delete_table('patients_userdata')
        
        # Deleting model 'Coupon'
        db.delete_table('patients_coupon')
        
        # Deleting model 'Profile'
        db.delete_table('patients_profile')
        
    
    
    models = {
        'patients.coupon': {
            'coupon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 9, 3, 8, 25, 50, 816079)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 9, 3, 8, 25, 50, 815941)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
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
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'target_weight': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'patients.userdata': {
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'waist': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        }
    }
    
    complete_apps = ['patients']
