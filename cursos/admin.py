from django.contrib import admin
from models import Curso, CursoDia, CursoDocente, CursoRegistro, CursoPago
from django.conf import settings

class CursoAdmin(admin.ModelAdmin):
	class Media:
		js = ('%stiny_mce/tiny_mce.js' % settings.STATIC_URL,
			'%sjs/admin.js' % settings.STATIC_URL
		)

		css = {
			'all': ('css/admin.css', )
		}

class CursoDiaAdmin(admin.ModelAdmin):
	class Media:
		js = ('%stiny_mce/tiny_mce.js' % settings.STATIC_URL,
			'%sjs/admin.js' % settings.STATIC_URL
		)

		css = {
			'all': ('css/admin.css', )
		}

class CursoDocenteAdmin(admin.ModelAdmin):
	class Media:
		js = ('%stiny_mce/tiny_mce.js' % settings.STATIC_URL,
			'%sjs/admin.js' % settings.STATIC_URL
		)

		css = {
			'all': ('css/admin.css', )
		}

class CursoRegistroAdmin(admin.ModelAdmin):
	list_filter = ('pago__curso', 'pago__method', 'pago__charged', 'pago__pais')
	search_fields = ('pago__nombre', 'pago__email')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'pago':
			for i in kwargs:
				print i
			kwargs['queryset'] = CursoPago.objects.filter(charged=True).order_by('nombre')

		return super(CursoRegistroAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class CursoPagoAdmin(admin.ModelAdmin):
	list_filter = ('curso', 'method', 'charged', 'pais')
	search_fields = ('nombre', 'email')
	list_display = ('nombre', 'email',)

admin.site.register(Curso, CursoAdmin)
admin.site.register(CursoDia, CursoDiaAdmin)
admin.site.register(CursoDocente, CursoDocenteAdmin)
admin.site.register(CursoRegistro, CursoRegistroAdmin)
admin.site.register(CursoPago, CursoPagoAdmin)
