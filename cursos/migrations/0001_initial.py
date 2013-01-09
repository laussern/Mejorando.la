# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Curso'
        db.create_table('cursos_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.TextField')()),
            ('precio', self.gf('django.db.models.fields.IntegerField')()),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.TextField')()),
            ('mapa', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('info_pago', self.gf('django.db.models.fields.TextField')()),
            ('activado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cursos', ['Curso'])

        # Adding model 'CursoDia'
        db.create_table('cursos_cursodia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')()),
            ('tema', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('temario', self.gf('django.db.models.fields.TextField')()),
            ('curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.Curso'])),
        ))
        db.send_create_signal('cursos', ['CursoDia'])

        # Adding model 'CursoDocente'
        db.create_table('cursos_cursodocente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('perfil', self.gf('django.db.models.fields.TextField')()),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.Curso'], blank=True)),
        ))
        db.send_create_signal('cursos', ['CursoDocente'])

        # Adding model 'CursoPago'
        db.create_table('cursos_cursopago', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.Curso'])),
            ('charged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cursos', ['CursoPago'])

        # Adding model 'CursoRegistro'
        db.create_table('cursos_cursoregistro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('pago', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.CursoPago'])),
        ))
        db.send_create_signal('cursos', ['CursoRegistro'])


    def backwards(self, orm):
        # Deleting model 'Curso'
        db.delete_table('cursos_curso')

        # Deleting model 'CursoDia'
        db.delete_table('cursos_cursodia')

        # Deleting model 'CursoDocente'
        db.delete_table('cursos_cursodocente')

        # Deleting model 'CursoPago'
        db.delete_table('cursos_cursopago')

        # Deleting model 'CursoRegistro'
        db.delete_table('cursos_cursoregistro')


    models = {
        'cursos.curso': {
            'Meta': {'object_name': 'Curso'},
            'activado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'direccion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'info_pago': ('django.db.models.fields.TextField', [], {}),
            'mapa': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.TextField', [], {}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'precio': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.TextField', [], {})
        },
        'cursos.cursodia': {
            'Meta': {'object_name': 'CursoDia'},
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cursos.Curso']"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tema': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'temario': ('django.db.models.fields.TextField', [], {})
        },
        'cursos.cursodocente': {
            'Meta': {'object_name': 'CursoDocente'},
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cursos.Curso']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'perfil': ('django.db.models.fields.TextField', [], {}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'cursos.cursopago': {
            'Meta': {'object_name': 'CursoPago'},
            'charged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cursos.Curso']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'cursos.cursoregistro': {
            'Meta': {'object_name': 'CursoRegistro'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pago': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cursos.CursoPago']"})
        }
    }

    complete_apps = ['cursos']