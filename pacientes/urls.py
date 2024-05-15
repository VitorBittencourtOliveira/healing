from django.urls import path
from pacientes.views import Home, EscolherHorario, AgendarHorario, MinhasConsultas, consulta, CancelarConsulta

urlpatterns = [
    path('home/', Home, name='home'),
    path('escolher_horario/<int:id_dados_medicos>', EscolherHorario, name='escolher_horario'),
    path('agendar_horario/<int:id_data_aberta>/', AgendarHorario, name="agendar_horario"),
    path('minhas_consultas/', MinhasConsultas, name="minhas_consultas"),
    path('consulta/<int:id_consulta>/', consulta, name="consulta"),
    path('cancelar_consulta/<int:id_consulta>/', CancelarConsulta, name="cancelar_consulta"),
]
