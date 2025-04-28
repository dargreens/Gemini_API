
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import google.generativeai as genai


# Create your views here.
def index(request):
    entrada='Enter User Info'
    if request.method=='POST': #if submit was clicked
        username=request.POST['username'] #what the user typed in
        password=request.POST['password']
        welcome=username #for display purposes
        user=authenticate(request, username=username, password=password)
        if user is not None:
            try:
                login(request, user)
                return render(request, 'weather.html', {'welcome': welcome})
            except:
                error_msg='Invalid username and/or psswd'
                return render(request, 'index.html', {'error_msg': error_msg})
        else:
            error_msg='Invalid username and/or psswd'            
            return render(request, 'index.html', {'error_msg': error_msg})
    
    return render(request, 'index.html', {'entrada': entrada})

def signup(request):
    welcome='signup successful: please keep your credentials safe'
    error_msg='please use at least 5 chars on each input'
    if request.method=='POST': 
        username=request.POST['username']
        email=request.POST['email']  
        password=request.POST['password']
        re_password=request.POST['Re-Type-Password']
        if (len(username)>=5 and len(password)>=5 and password==re_password):
            try:
                user=User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return render(request, 'weather.html', {'welcome': welcome})
            except:
                error_msg='error creating account'
                return render(request, 'signup.html', {'error_msg': error_msg})
        else:
           return render(request, 'signup.html', {'error_msg': error_msg})     



    return render(request, 'signup.html')

def weather(request):

    return render(request, 'weather.html')
    
@csrf_exempt    
def jsonurl(request):
    if request.method=='POST':
        try:
            #get user_input (stored in json) from fetch() in javascript
            get_user_input=json.loads(request.body)
            prompt=get_user_input["link"] 
            
            #if a form element is used w/ method=POST, get data
            #convert_form_data_to_json=json.dumps(request.POST)
            #output_to_json=json.loads(convert_form_data_to_json)        
        
            #genai w/ gemini
            genai.configure(api_key="AIzaSyAH-t-9elGqgm9kQGuhFkyfW_djQyv7zr4")
            model = genai.GenerativeModel("gemini-1.5-flash-8b")            
            response = model.generate_content(f"{prompt}")
            answer= response.text
            
            return JsonResponse({'content':answer})
            
        
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'invalid data sent'}, status=400)
        
        

    else:
        return JsonResponse({'error':'invalid request method'}, status=405)
