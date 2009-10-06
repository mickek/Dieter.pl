# -*- coding: utf-8 -*-    

from south.db import db
from django.db import models
from dieter.diet.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Diet.name'
        db.add_column('diet_diet', 'name', orm['diet.diet:name'])
        
        # Changing field 'Diet.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User'], null=True))
        db.alter_column('diet_diet', 'user_id', orm['diet.diet:user'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Diet.name'
        db.delete_column('diet_diet', 'name')
        
        # Changing field 'Diet.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User']))
        db.alter_column('diet_diet', 'user_id', orm['diet.diet:user'])
        
    
    
    models = {
        'diet.meal': {
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diet.DayPlan']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sequence_no': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 6, 23, 19, 23, 769801)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 6, 23, 19, 23, 769689)'}),
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
        'diet.food': {
            'calories': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'diet.dayplan': {
            'diet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diet.Diet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence_no': ('django.db.models.fields.IntegerField', [], {})
        },
        'diet.diet': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_diet'", 'null': 'True', 'to': "orm['diet.Diet']"}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        }
    }
    
    complete_apps = ['diet']
