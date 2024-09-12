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

@login_required
def home(request):
    # Fetch the user's questionnaire result
    result = QuestionnaireResult.objects.filter(user=request.user).first()
    
    # Pass the questionnaire result to the template
    return render(request, 'home.html', {'user_questionnaire': result})

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
            print(f"Received data: {data}")  # Log the incoming data

            username = data.get('username')
            selected_team = data.get('selectedOption')
            selected_topic = data.get('selectedSubOption')
            comfort_level = data.get('selectedComfortLevel')
            answers = data.get('answers', [])  # Retrieve answers

            # Fetch user and their questionnaire result
            user = User.objects.get(username=username)
            result, created = QuestionnaireResult.objects.get_or_create(user=user)

            # Update the result with the answers and mark it as completed
            result.favorite_team = selected_team
            result.favorite_topic = selected_topic
            result.comfort_level = comfort_level
            result.completed = True
            result.save()

            # Save detailed answers
            DetailedAnswer.objects.filter(result=result).delete()  # Clear old answers
            for answer in answers:
                DetailedAnswer.objects.create(
                    result=result,
                    question=answer['question'],
                    answer=answer['answer']
                )

            print(f"Successfully saved answers for {username}")  # Log success
            return JsonResponse({'status': 'success'})
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