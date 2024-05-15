from django.urls import path
from medicos.views import CadastroMedico, AbrirHorario, DelHorario, ConsultasMedico, ConsultaAreaMedico, FinalizarConsulta, AddDocumento, DelDocumento, Dashboard

urlpatterns = [
    path('cadastro_medico/', CadastroMedico, name="cadastro_medico"),
    path('abrir_horario/', AbrirHorario, name="abrir_horario"),
    path('del_horario/<int:id_horario>/', DelHorario, name="del_horario"),
    path('consultas_medico/', ConsultasMedico, name="consultas_medico"),
    path('consulta_area_medico/<int:id_consulta>/', ConsultaAreaMedico, name="consulta_area_medico"),
    path('finalizar_consulta/<int:id_consulta>/', FinalizarConsulta, name="finalizar_consulta"),
    path('add_documento/<int:id_consulta>/', AddDocumento, name="add_documento"),
    path('del_documento/<int:id_consulta>/<int:id_documento>', DelDocumento, name="del_documento"),
    path('dashboard/', Dashboard, name="dashboard")
]
