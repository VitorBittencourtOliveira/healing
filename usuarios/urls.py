from django.urls import path
from usuarios.views import Cadastro, Login, Logout

urlpatterns = [
    path('cadastro/', Cadastro, name="cadastro"),
    path('login/', Login, name="login"),
    path('logout/', Logout, name="logout"),
]
