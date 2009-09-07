# -*- coding: utf-8 -*-    

from south.db import db
from django.db import models
from dieter.diet.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Meal'
        db.create_table('diet_meal', (
            ('name', orm['diet.Meal:name']),
            ('sequence_no', orm['diet.Meal:sequence_no']),
            ('day', orm['diet.Meal:day']),
            ('unit_type', orm['diet.Meal:unit_type']),
            ('type', orm['diet.Meal:type']),
            ('id', orm['diet.Meal:id']),
            ('quantity', orm['diet.Meal:quantity']),
        ))
        db.send_create_signal('diet', ['Meal'])
        
        # Adding model 'Diet'
        db.create_table('diet_diet', (
            ('user', orm['diet.Diet:user']),
            ('state', orm['diet.Diet:state']),
            ('id', orm['diet.Diet:id']),
            ('start_date', orm['diet.Diet:start_date']),
        ))
        db.send_create_signal('diet', ['Diet'])
        
        # Adding model 'Food'
        db.create_table('diet_food', (
            ('unit_type', orm['diet.Food:unit_type']),
            ('calories', orm['diet.Food:calories']),
            ('id', orm['diet.Food:id']),
            ('name', orm['diet.Food:name']),
        ))
        db.send_create_signal('diet', ['Food'])
        
        # Adding model 'DayPlan'
        db.create_table('diet_dayplan', (
            ('sequence_no', orm['diet.DayPlan:sequence_no']),
            ('id', orm['diet.DayPlan:id']),
            ('diet', orm['diet.DayPlan:diet']),
        ))
        db.send_create_signal('diet', ['DayPlan'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Meal'
        db.delete_table('diet_meal')
        
        # Deleting model 'Diet'
        db.delete_table('diet_diet')
        
        # Deleting model 'Food'
        db.delete_table('diet_food')
        
        # Deleting model 'DayPlan'
        db.delete_table('diet_dayplan')
        
    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 9, 7, 17, 50, 10, 897488)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 9, 7, 17, 50, 10, 897354)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'diet.diet': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        }
    }
    
    complete_apps = ['diet']
