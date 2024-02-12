from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import TextFile, UploadFileForm
import yaml, re
from django.conf import settings
import os
  
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
            uploaded_file = form.save()
            input_file_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_file.file))
            output_file_path = os.path.join(settings.MEDIA_ROOT, 'converted_yaml.yaml')
            convert_text_to_yaml(input_file_path, output_file_path)
            print('Form is valid')
            return render(request, "upload_success.html", {"form": form})
        else:
            print("Form not valid")
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})

def convert_text_to_yaml(input_file_path, output_file_path):
    questions = []

    with open(input_file_path, 'r') as input_file:
        current_question = None
        for line in input_file:
            line = line.strip()
            if line.startswith("question:"):
                if current_question:
                    #questions = []
                    questions.append(current_question)
                current_question = {"question": line.split(":", 1)[1].split(";")[0].strip()}
            elif line.startswith("marks:"):
                current_question["marks"] = int(line.split(":", 1)[1].split(";")[0].strip())
            elif line.startswith("option:"):
                if "answers" not in current_question:
                    current_question["answers"] = []
                current_question["answers"].append(line.split(":", 1)[1].split(";")[0].strip())
            elif line.startswith("correct:"):
                current_question["correct"] = line.split(":", 1)[1].split(";")[0].strip()
                
    if current_question:
        questions.append(current_question)

    with open(output_file_path, 'w') as output_file:
        yaml.dump(questions, output_file, default_flow_style=False, sort_keys=False)

def download_yaml(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'converted_yaml.yaml')
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type = 'application/yaml')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response
#input_file_path = r'C:\Users\admin\Desktop\sample.txt'
#output_file_path = r'C:\Users\admin\Desktop\djpro\txtyaml\convertedyaml.yaml'
#convert_text_to_yaml(input_file_path, output_file_path)