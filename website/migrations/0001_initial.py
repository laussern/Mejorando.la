# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Setting'
        db.create_table('website_setting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('website', ['Setting'])

        # Adding model 'Video'
        db.create_table('website_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('embed_code', self.gf('django.db.models.fields.TextField')()),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('participantes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('activado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audio', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('website', ['Video'])

        # Adding model 'VideoComentario'
        db.create_table('website_videocomentario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('autor_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('autor_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'])),
        ))
        db.send_create_signal('website', ['VideoComentario'])

        # Adding model 'Curso'
        db.create_table('website_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('activado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('website', ['Curso'])

        # Adding model 'Conferencia'
        db.create_table('website_conferencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('ubicacion', self.gf('django.db.models.fields.TextField')()),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('num_asistentes', self.gf('django.db.models.fields.IntegerField')()),
            ('num_horas_video', self.gf('django.db.models.fields.IntegerField')()),
            ('num_conferencias', self.gf('django.db.models.fields.IntegerField')()),
            ('activado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('website', ['Conferencia'])

        # Adding model 'RegistroCurso'
        db.create_table('website_registrocurso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('pago', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('curso', self.gf('django.db.models.fields.TextField')()),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personas', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total', self.gf('django.db.models.fields.FloatField')()),
            ('descuento', self.gf('django.db.models.fields.FloatField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='paypal', max_length=100)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('website', ['RegistroCurso'])

        # Adding model 'RegistroConferencia'
        db.create_table('website_registroconferencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('website', ['RegistroConferencia'])

        # Adding model 'MailRegistroCurso'
        db.create_table('website_mailregistrocurso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('website', ['MailRegistroCurso'])


    def backwards(self, orm):
        # Deleting model 'Setting'
        db.delete_table('website_setting')

        # Deleting model 'Video'
        db.delete_table('website_video')

        # Deleting model 'VideoComentario'
        db.delete_table('website_videocomentario')

        # Deleting model 'Curso'
        db.delete_table('website_curso')

        # Deleting model 'Conferencia'
        db.delete_table('website_conferencia')

        # Deleting model 'RegistroCurso'
        db.delete_table('website_registrocurso')

        # Deleting model 'RegistroConferencia'
        db.delete_table('website_registroconferencia')

        # Deleting model 'MailRegistroCurso'
        db.delete_table('website_mailregistrocurso')


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
            'audio': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'embed_code': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'participantes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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