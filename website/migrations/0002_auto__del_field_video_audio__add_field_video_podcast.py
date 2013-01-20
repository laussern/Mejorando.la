# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Video.audio'
        db.delete_column('website_video', 'audio')

        # Adding field 'Video.podcast'
        db.add_column('website_video', 'podcast',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Video.audio'
        db.add_column('website_video', 'audio',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Deleting field 'Video.podcast'
        db.delete_column('website_video', 'podcast')


    models = {
        'website.conferencia': {
            'Meta': {'object_name': 'Conferencia'},
            'activado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'num_asistentes': ('django.db.models.fields.IntegerField', [], {}),
            'num_conferencias': ('django.db.models.fields.IntegerField', [], {}),
            'num_horas_video': ('django.db.models.fields.IntegerField', [], {}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'ubicacion': ('django.db.models.fields.TextField', [], {})
        },
        'website.curso': {
            'Meta': {'object_name': 'Curso'},
            'activado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'website.mailregistrocurso': {
            'Meta': {'object_name': 'MailRegistroCurso'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'website.registroconferencia': {
            'Meta': {'object_name': 'RegistroConferencia'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.registrocurso': {
            'Meta': {'object_name': 'RegistroCurso'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'curso': ('django.db.models.fields.TextField', [], {}),
            'descuento': ('django.db.models.fields.FloatField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pago': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personas': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'paypal'", 'max_length': '100'}),
            'total': ('django.db.models.fields.FloatField', [], {})
        },
        'website.setting': {
            'Meta': {'object_name': 'Setting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'activado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'embed_code': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'participantes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podcast': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'website.videocomentario': {
            'Meta': {'object_name': 'VideoComentario'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'autor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'autor_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['website']