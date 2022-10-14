from django.shortcuts import render, redirect
from services.firebase import Firebase
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from web.forms import MapForm

class ContributeView(TemplateView):
    def __init__(self):
        self.template_name = 'contribute.html'
    
    def get(self, request):
        fb = Firebase()
        fb.login_token(request.session['fbtoken'])
        return render(request, self.template_name)

    def post(self, request):
        rq = request.POST.dict()
        if 'logout' in rq and rq['logout'] == '1':
            logout(request)
            return redirect('/')
        return render(request, self.template_name)

class LoginView(TemplateView):
    def __init__(self):
        self.template_name = 'login.html'
        self.ctx = ''

    def get(self, request):
        return render(request, self.template_name, {'ctx': self.ctx})

    def post(self, request):
        rq = request.POST.dict()
        if "email" in rq and "password" in rq:
            email = rq['email']
            password = rq['password']
            user = authenticate(username=email, email=email, password=password)
            if user is not None:
                login(request, user)
                fb = Firebase()
                fb.login(email, password)
                request.session['fbtoken'] = fb.user['refreshToken']
                return redirect('/contribute/')
            self.ctx = "Invalid email or password."
        return render(request, self.template_name, {'ctx': self.ctx})

class RegisterView(TemplateView):
    def __init__(self):
        self.template_name = 'register.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        rq = request.POST.dict()
        self.ctx = "Fill all fields!"
        if "email" in rq and "password" in rq and "confirm-password" in rq:
            email = rq['email']
            password = rq['password']
            self.ctx = "Passwords do not match."
            if password == rq["confirm-password"]:  
                self.ctx = "Password must be at least 8 characters."
                if len(password) >= 8:
                    self.ctx = "Enter a valid email address."
                    if "@" in email:
                        self.ctx = "Email already in use."
                        try:
                            user = User.objects.create_user(email, email, password)
                            user.save()
                        except:
                            return render(request, self.template_name, {'ctx': self.ctx})
                        user = authenticate(username=email, email=email, password=rq["password"])
                        if user is not None:
                            login(request, user)
                            fb = Firebase()
                            fb.register(email, password)
                            request.session['fbtoken'] = fb.user['refreshToken']
                            return redirect('/contribute/')
        return render(request, self.template_name, {'ctx': self.ctx})

class AnimalsView(TemplateView):
    def __init__(self):
        self.template_name = 'animals.html'
        self.ctx = ''

    def get(self, request):
        return render(request, self.template_name, {'form': MapForm})

    def post(self, request):
        rq = request.POST.dict()
        print(rq)
        return render(request, self.template_name, {'form': MapForm})
