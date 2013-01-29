# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CursoDocente.curso'
        db.delete_column('cursos_cursodocente', 'curso_id')

        # Adding M2M table for field cursos on 'CursoDocente'
        db.create_table('cursos_cursodocente_cursos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cursodocente', models.ForeignKey(orm['cursos.cursodocente'], null=False)),
            ('curso', models.ForeignKey(orm['cursos.curso'], null=False))
        ))
        db.create_unique('cursos_cursodocente_cursos', ['cursodocente_id', 'curso_id'])


    def backwards(self, orm):
        # Adding field 'CursoDocente.curso'
        db.add_column('cursos_cursodocente', 'curso',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['cursos.Curso'], blank=True),
                      keep_default=False)

        # Removing M2M table for field cursos on 'CursoDocente'
        db.delete_table('cursos_cursodocente_cursos')


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
            'slug': ('django.db.models.fields.TextField', [], {}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
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
            'cursos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cursos.Curso']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ua': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'cursos.cursoregistro': {
            'Meta': {'object_name': 'CursoRegistro'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pago': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cursos.CursoPago']"})
        }
    }

    complete_apps = ['cursos']