from django.contrib import admin
from models import Curso, CursoDia, CursoDocente, CursoRegistro
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

admin.site.register(Curso, CursoAdmin)
admin.site.register(CursoDia, CursoDiaAdmin)
admin.site.register(CursoDocente, CursoDocenteAdmin)
admin.site.register(CursoRegistro)
