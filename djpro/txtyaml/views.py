from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import TextFile, UploadFileForm
import yaml, re
  
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
def home(request): 
    return render(request, 'home.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')

def form(request):
    form = TextFile()
    context = {'form':form}
    return render(request, 'form.html', context)

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            print('Form is valid')
            return HttpResponse("success")
        else:
            print("Form not valid")
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})
    
def convert_to_yaml(text_content):
    yaml_data = {"questions": []}
    lines = text_content.split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(';')
        question = parts[0]
        marks = int(parts[1])
        options = parts[2:-1]
        correct_answer = parts[-1]

        question_dict = {
            "description": question,
            "marks": marks,
            "options": options,
            "correct_answer": correct_answer
        }

        yaml_data["questions"].append(question_dict)

    return yaml_data
