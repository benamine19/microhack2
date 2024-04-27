from django.shortcuts import render
from users.serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from AI.TaskEvaluation import TaskEvaluation
from django.http import JsonResponse

from AI.VoiceToTask import VoiceToTask
# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializerChef

# il faut que l'utilsateur soit le chef pour etre valaible d'ajouter des employer
@api_view(['POST'])
def chef_add_employe(request):
    chef_id = request.data.get('chef_id')
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    profile_pic = request.data.get('profile_pic')
    if not (username and password and email):
        return Response({"error": "Please provide username, password, and email for the new employee."},
                        status=status.HTTP_400_BAD_REQUEST)
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken. Please choose a different username."},
                        status=status.HTTP_400_BAD_REQUEST)
    chef=get_object_or_404(Chef,id=chef_id)
    user=User.objects.create(username=username,email=email,profile_pic=profile_pic,role='employee')
    user.set_password(password)
    user.save()
    employe=Employe.objects.create(
            user=user,
            chef=chef,
    )
    response="Succed to create employee"
    return Response({
            'response':response,
            'data 1':UserSerializer(user).data
            } ,status=status.HTTP_200_OK)


# ajouter une tache par le chef 
@api_view(['POST'])
def chef_add_tache_form(request):
    chef_id = request.data.get('chef_id')
    description = request.data.get('description')
    etat = request.data.get('etat')
    importance = request.data.get('importance')
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and description and etat and importance):
        print('da5lt lhadi')
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)
    tache = Tache.objects.create(
                chef=chef,
                description=description,
                etat=etat,
                importance=importance
            ) 
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def chef_add_tache_audio(request):
    chef_id = request.data.get('chef_id')
    audio = request.FILES.get('audio')
    #return Response( status=status.HTTP_201_CREATED)
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and audio):
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)   
         
    file_name = 'TaskAudio.m4a'  # Example: You may use a unique file name based on time or user ID
        
    # Specify the path where you want to save the audio file
    save_path = 'Audio/' + file_name


    # Save the audio data to a file
    with open(save_path, 'wb') as destination:
        for chunk in audio.chunks():
            destination.write(chunk)
    
    Task = VoiceToTask(save_path)
    
    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)
      
    
    tache = Tache.objects.create(
                chef=chef,
                importance = Task["Importance"],
                description=Task["Task"],
                duration = Task["Duration"],
            ) 
    
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)



# # le chef ajouter des emploie pour une tache  
# @api_view(['POST'])
# def chef_add_tache(request):
#     chef_id = request.data.get('chef_id')
#     employes_id = request.data.get('employes_id', [])
#     etat = request.data.get('etat')
#     importance = request.data.get('importance')
#     # print("etat",etat)
#     # Vérifier si tous les champs requis sont présents dans la requête
#     if not (chef_id ):
#         return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
#                         status=status.HTTP_400_BAD_REQUEST)
#     # Récupérer le chef associé à l'identifiant fourni
#  chef = get_object_or_404(Chef, id=chef_id)
#  tache = Tache.objects.create(
#              chef=chef,
#              description=description,
#              etat=etat,
#              importance=importance
#          )
#  response_data = {
#          'message': 'Tâche créée avec succès.',
#          'data': TacheSerializer(tache).data
#      }
#  return Response(response_data, status=status.HTTP_201_CREATED)




# le chef ajouter des emploie pour une tache  
@api_view(['POST'])
def chef_modifier_tache(request):
    chef_id = request.data.get('chef_id')
    description = request.data.get('description')
    etat = request.data.get('etat')
    importance = request.data.get('importance')
    # print("etat",etat)
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and description and etat and importance):
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)
    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)
    tache = Tache.objects.create(
                chef=chef,
                description=description,
                etat=etat,
                importance=importance
            )
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)



# Associate tasks manually to employes 
@api_view(['POST'])
def associate_tasks_to_employes_manually(request):
    employes_id = request.data.get('employes_id', [])
    tache_id = request.data.get('tache_id')
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (employes_id and tache_id):
        return Response({"error": "Veuillez fournir employes_id et tache_id."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer la tâche associée à l'identifiant fourni
    tache = get_object_or_404(Tache, id=tache_id)

    # Récupérer la liste des employés associés aux identifiants fournis
    for emp_id in employes_id:
        employe = get_object_or_404(Employe, id=emp_id)
        tache.employes.add(employe)

    response_data = {
        'message': 'Tâche associée aux employés avec succès.',
        'data': TacheSerializer(tache).data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def associate_tasks_to_employes_automaticaly(request):
    employes_id = request.data.get('employes_id', [])
    tache_id = request.data.get('tache_id')
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (employes_id and tache_id):
        return Response({"error": "Veuillez fournir employes_id et tache_id."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer la tâche associée à l'identifiant fourni
    tache = get_object_or_404(Tache, id=tache_id)

    # Récupérer la liste des employés associés aux identifiants fournis
    for emp_id in employes_id:
        employe = get_object_or_404(Employe, id=emp_id)
        tache.employes.add(employe)

    response_data = {
        'message': 'Tâche associée aux employés avec succès.',
        'data': TacheSerializer(tache).data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def chef_modifier_tache(request, tache_id):
        chef_id = request.data.get('chef_id')
        description = request.data.get('description')
        etat = request.data.get('etat')
        importance = request.data.get('importance')
        
        # Vérifier si tous les champs requis sont présents dans la requête
        if not (chef_id and description and etat and importance):
            return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer le chef associé à l'identifiant fourni
        chef = get_object_or_404(Chef, id=chef_id)
        
        # Récupérer la tâche à modifier
        tache = get_object_or_404(Tache, id=tache_id)
        
        # Vérifier si le chef est le propriétaire de la tâche
        if tache.chef != chef:
            return Response({"error": "Vous n'êtes pas autorisé à modifier cette tâche."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Mettre à jour les champs de la tâche
        tache.description = description
        tache.etat = etat
        tache.importance = importance
        tache.save()
        
        response_data = {
            'message': 'Tâche modifiée avec succès.',
            'data': TacheSerializer(tache).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

        # le chef ajoute des employés à une tâche
@api_view(['POST'])
def chef_add_employes_to_tache(request, tache_id):
            chef_id = request.data.get('chef_id')
            employes_id = request.data.get('employes_id', [])
            
            # Vérifier si tous les champs requis sont présents dans la requête
            if not (chef_id and employes_id):
                return Response({"error": "Veuillez fournir chef_id et employes_id."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Récupérer le chef associé à l'identifiant fourni
            chef = get_object_or_404(Chef, id=chef_id)
            
            # Récupérer la tâche à laquelle ajouter les employés
            tache = get_object_or_404(Tache, id=tache_id)
            
            # Vérifier si le chef est le propriétaire de la tâche
            if tache.chef != chef:
                return Response({"error": "Vous n'êtes pas autorisé à modifier cette tâche."},
                                status=status.HTTP_403_FORBIDDEN)
            
            # Ajouter les employés à la tâche
            for emp_id in employes_id:
                employe = get_object_or_404(Employe, id=emp_id)
                tache.employes.add(employe)
            
            response_data = {
                'message': 'Employés ajoutés à la tâche avec succès.',
                'data': TacheSerializer(tache).data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
# le chef supprime des employés d'une tâche    
@api_view(['POST'])
def chef_supprimer_tache(request):
                chef_id = request.data.get('chef_id')
                tache_id = request.data.get('tache_id')
                # Vérifier si le chef_id est fourni
                if not chef_id:
                    return Response({"error": "Veuillez fournir chef_id."},
                                    status=status.HTTP_400_BAD_REQUEST)
                # Récupérer le chef associé à l'identifiant fourni
                chef = get_object_or_404(Chef, id=chef_id)
                
                # Récupérer la tâche à supprimer
                tache = get_object_or_404(Tache, id=tache_id)
                
                # Vérifier si le chef est le propriétaire de la tâche
                if tache.chef != chef:
                    return Response({"error": "Vous n'êtes pas autorisé à supprimer cette tâche."},
                                    status=status.HTTP_403_FORBIDDEN)
                
                # Supprimer la tâche
                tache.delete()
                
                response_data = {
                    'message': 'Tâche supprimée avec succès.'
                }
                return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_all_taches(request):
    taches = Tache.objects.all()
    serializer = TacheSerializer(taches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def get_tache_emploie(request):
    user_id = request.data.get('user_id')
    user=get_object_or_404(User,id=user_id)
    employe=Employe.objects.filter(user=user).first()
    emploie = get_object_or_404(Employe, id=emp_id)
    taches = Tache.objects.all().filter(employes=emploie)
    serializer = TacheSerializer(taches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_all_employes(request):
    if request.method == 'GET':
        employes = Employe.objects.all()
        employes_list = []

        for employe in employes:
            emploie_data = {
                'emploie_id': employe.id,
                'user_id': employe.user.id,
                'username': employe.user.first_name,
                'status': employe.status,
                'rank': employe.rank,
                'email': employe.user.email,
            }

            # Vérifier si l'utilisateur a un profile_pic associé
            if employe.user.profile_pic:
                emploie_data['profile_pic'] = employe.user.profile_pic.url
            else:
                emploie_data['profile_pic'] = None  # Aucune image de profil

            employes_list.append(emploie_data)

        return JsonResponse({'employes': employes_list})

@api_view(['POST'])
def add_task_response(request):
    if request.method == 'POST':
        # Assuming the form field name for the image is 'image'
        tache_id = request.data.get('tache_id')
        image_file = request.FILES.get('image')
        audio_file = request.FILES.get('audio')
        employes_id = request.data.get('employes_id', [])
        task = get_object_or_404(Tache, id=tache_id)
        # verifier si l'employe est associé à la tache
        if image_file:
            task_response = TaskResponse(task=task,image=image_file,audio = audio_file,percentage=0)
            task_response.save()
            Evaluation = TaskEvaluation(task.description,task_response.image.url)
            print(Evaluation)
            task_response.percentage = Evaluation["percentage"] 
            percentage=Evaluation["percentage"] 
            
            if (percentage>90):
                task.etat='finish'
                task.save()
                employes = task.employes.all()
                for employe in employes:
                    employe.rank += 10
                    employe.save()
        
            response_data = {
                    'message': 'Tâche supprimée avec succès.',
                    'data': TacheResponseSerializer(task_response).data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No image"},
                    status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No image"},
                    status=status.HTTP_400_BAD_REQUEST)



