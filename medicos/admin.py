from django.contrib import admin
from medicos.models import Especialidades, DadosMedico, DatasAbertas

class ListandoEspecialidades(admin.ModelAdmin):
    list_display = ("id", "especialidade",)
    list_display_links = ("id", "especialidade",)
    list_per_page = 20
    
class ListandoDatasAbertas(admin.ModelAdmin):
    list_display = ("id", "data","medico","agendado")
    list_display_links = ("id", "data",)
    list_per_page = 20
    
    def medico(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    medico.short_description = 'Médico'

class ListandoDadosMedico(admin.ModelAdmin):
    list_display = ("id", "nome","especialidade")
    list_display_links = ("id", "nome",)
    list_per_page = 20
    
admin.site.register(Especialidades, ListandoEspecialidades)
admin.site.register(DadosMedico, ListandoDadosMedico)
admin.site.register(DatasAbertas, ListandoDatasAbertas)