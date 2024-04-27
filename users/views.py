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

from AI.VoiceToTask import GetNeededSpecialities, VoiceToTask

# Views.

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializerChef

###Add An employee by the chef
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


# Add a task by the chef
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

# add an audio task by the chef and convert it into text AI and Convert it to a task using AI 
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


#midify task by the manager
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

# Associate tasks Automaticaly to employes using AI by estimation the number of workers needed in each field
@api_view(['POST'])
def associate_tasks_to_employes_automaticaly(request):
    tache_id = request.data.get('tache_id')
    tache = get_object_or_404(Tache, id=tache_id)
    NeededSpecialities = GetNeededSpecialities(tache.description)
    if(NeededSpecialities["Plumber"]):
        Plumbers = Employe.objects.filter(Q(speciality="Plumber" )).order_by('rank')
        if(Plumbers.exists()):
            taskPlumber = Plumbers[:NeededSpecialities["Plumber"]]
            for plumber in taskPlumber:
                tache.employes.add(plumber)
    if(NeededSpecialities["General"]):
        Genrals = Employe.objects.filter(Q(speciality="General"))
        print(Employe.objects.count())
        if(Genrals.exists()):
            taskGenral = Genrals[:NeededSpecialities["General"]]
            for Genral in taskGenral:
                print(Genral)
                tache.employes.add(Genral)
    if(NeededSpecialities["Carpenter"]):
        Carpenters = Employe.objects.filter(Q(speciality="Carpenter" )).order_by('rank')
        if(Carpenters.exists()):
            taskCarpenter = Carpenters[:NeededSpecialities["Carpenter"]]
            for carpenter in taskCarpenter:
                tache.employes.add(carpenter)
    if(NeededSpecialities["Mason"]):
        Masons = Employe.objects.filter(Q(speciality="Mason" )).order_by('rank')
        if(Masons.exists()):
            taskMason = Masons[:NeededSpecialities["Mason"]]
            for mason in taskMason:
                tache.employes.add(mason)
    tache.save()

    response_data = {
        'message': 'Tâche associée automatiquement aux employés avec succès.',
        'data': TacheSerializer(tache).data
    }
    return Response(response_data, status=status.HTTP_200_OK)

# le chef modifie une tâche
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
        employes = Employe.objects.all()
        serializer = EmployeSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_task_response(request):
    if request.method == 'POST':
        # Assuming the form field name for the image is 'image'
        tache_id = request.data.get('tache_id')
        image_file = request.FILES.get('image')
        audio_file = request.FILES.get('audio')
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



