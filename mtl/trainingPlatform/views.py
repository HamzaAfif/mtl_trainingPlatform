from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from .models import QuestionnaireResult, DetailedAnswer, User
import os
from django.conf import settings

@login_required
def home(request):
    
    result = QuestionnaireResult.objects.filter(user=request.user).first()

   
    json_file_path = os.path.join(settings.BASE_DIR, 'plan.json')


    with open(json_file_path, 'r') as file:
        plan_data = json.load(file)

 
    user_team = result.favorite_team.lower()  
    user_topic = result.favorite_topic.replace(" ", "_")  
    user_level = result.comfort_level.lower()  

 
    courses = plan_data.get(user_team, {}).get(user_topic, {}).get(user_level, [])

    return render(request, 'home.html', {
        'user_questionnaire': result,
        'courses': courses
    })



def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@staff_member_required
def view_answers(request):
    users = User.objects.all()
    results = QuestionnaireResult.objects.all()

    # Prepare a list of users and their questionnaire status
    user_data = []
    for user in users:
        result = results.filter(user=user).first()
        if result:
            user_data.append({
                'id': user.id,  # Include the user ID here
                'username': user.username,
                'last_name' : user.last_name,
                'first_name' : user.first_name,
                'favorite_team': result.favorite_team,
                'favorite_topic': result.favorite_topic,
                'comfort_level': result.comfort_level,
                'completed': result.completed,
                'result_id': result.id
            })
        else:
            user_data.append({
                'id': user.id,  # Include the user ID here as well
                'username': user.username,
                'first_name' : user.first_name,
                'favorite_team': 'N/A',
                'favorite_topic': 'N/A',
                'comfort_level': 'N/A',
                'completed': False,
                'result_id': None
            })

    return render(request, 'view_answers.html', {'user_data': user_data})

@csrf_exempt
def save_answers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")  

            username = data.get('username')
            selected_team = data.get('selectedOption')
            selected_topic = data.get('selectedSubOption')
            comfort_level = data.get('selectedComfortLevel')
            answers = data.get('answers', [])  

            
            user = User.objects.get(username=username)
            result, created = QuestionnaireResult.objects.get_or_create(user=user)

            
            result.favorite_team = selected_team
            result.favorite_topic = selected_topic
            result.comfort_level = comfort_level
            result.completed = True
            result.save()

            
            total_score = 0
             

            DetailedAnswer.objects.filter(result=result).delete()  
            for answer in answers:
                answer_value = answer['answer']
                
                if answer_value == 'Beginner':
                    total_score += 1

                elif answer_value == 'Intermediate':
                    total_score += 2

                elif answer_value == 'Expert':
                    total_score += 3

            
                
                DetailedAnswer.objects.create(
                    result=result,
                    question=answer['question'],
                    answer=answer_value
                )

            
            if total_score <= (1.5 * len(answers)):  
                user_level = 'Beginner'
            elif total_score <= (2 * len(answers)):  
                user_level = 'Intermediate'
            else:  
                user_level = 'Expert'

            
            result.comfort_level = user_level
            result.save()

            print(f"Successfully saved answers for {username}, determined level: {user_level}")
            return JsonResponse({'status': 'success', 'level': user_level})
        except Exception as e:
            print(f"Error: {e}")  # Log the error
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def reset_answers(request, result_id):
    result = get_object_or_404(QuestionnaireResult, id=result_id)

    # Reset fields to default or empty values
    result.favorite_team = ''  # Or some default value if empty strings are allowed
    result.favorite_topic = ''
    result.comfort_level = ''
    result.completed = False
    result.save()

    messages.success(request, "Answers have been reset successfully.")
    return redirect('view_answers')

def view_detailed_answers(request, result_id):
    result = get_object_or_404(QuestionnaireResult, id=result_id)
    
    answers = result.answers.all()
    
    return render(request, 'view_detailed_answers.html', {'result': result, 'answers': answers})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User account deleted successfully.")
        return redirect('view_answers')  

def passwordChange(request):
    logout(request)
    return redirect('login')