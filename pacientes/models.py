from django.db import models
from django.contrib.auth.models import User
from medicos.models import DatasAbertas
from datetime import datetime

class Consulta(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')
    )
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)
    
    @property
    def diferenca_dias(self):
        try:
            diferenca = (self.data_aberta.data.date() - datetime.now().date()).days
            return diferenca
        except AttributeError:
            return None
    
    def __str__(self):
        return f"{self.paciente.first_name} {self.paciente.last_name}"

class Documento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.titulo