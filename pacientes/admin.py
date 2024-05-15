from django.contrib import admin
from pacientes.models import Consulta, Documento

class ListandoConsultas(admin.ModelAdmin):
    list_display = ("id", "nome_paciente", "data_consulta", "status",)
    list_display_links = ("id", "nome_paciente", "data_consulta", "status",)
    search_fields = ('paciente__first_name', 'paciente__last_name',)
    list_filter = ("status",)
    list_per_page = 20
    
    def nome_paciente(self, obj):
        return obj.paciente.first_name + ' ' + obj.paciente.last_name
    nome_paciente.short_description = 'Paciente'
    
    def data_consulta(self, obj):
        return obj.data_aberta.data.strftime("%d/%m/%Y às %H:%M")
    data_consulta.short_description = 'Data da Consulta'
    
class ListandoDocumentos(admin.ModelAdmin):
    list_display = ("id", "paciente_da_consulta", "titulo",)
    list_display_links = ("id", "paciente_da_consulta", "titulo",)
    search_fields = ('consulta__paciente__first_name', 'consulta__paciente__last_name',)
    list_per_page = 20
    
    def paciente_da_consulta(self, obj):
        return obj.consulta
    paciente_da_consulta.short_description = 'Paciente'

admin.site.register(Consulta, ListandoConsultas)
admin.site.register(Documento, ListandoDocumentos)