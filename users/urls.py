from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns =[
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),    
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('RegisterViewChef/', RegisterView.as_view(), name='RegisterView'),
    path('chef_add_employe/', chef_add_employe, name='chef_add_employe'),
    path('chef_add_tache_form/', chef_add_tache_form, name='chef_add_tache_form'),
    path('chef_add_tache_audio/', chef_add_tache_audio, name='chef_add_tache_audio'),
    path('associate_tasks_to_employes_manually/', associate_tasks_to_employes_manually, name='associate_tasks_to_employes_manually'),
    path('chef_add_tache_form/', chef_add_tache_form, name='chef_add_tache_form'),
    path('chef_add_tache_audio/', chef_add_tache_audio, name='chef_add_tache_audio'),
    path('associate_tasks_to_employes_manually/', associate_tasks_to_employes_manually, name='associate_tasks_to_employes_manually'),
    path('chef_modifier_tache/', chef_modifier_tache, name='chef_modifier_tache'),
    path('chef_add_employes_to_tache/', chef_add_employes_to_tache, name='chef_add_employes_to_tache'),
    path('get_all_taches/', get_all_taches, name='get_all_taches'),
    path('get_all_employes/', get_all_employes, name='get_all_employes'),  
    path('get_all_taches/', get_all_taches, name='get_all_taches'),
    path('get_all_employes/', get_all_employes, name='get_all_employes'),     
    path('add_task_response/', add_task_response, name='add_task_response'),     
]