from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.utils import timezone
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class ContributeView(TemplateView):
    def __init__(self):
        self.template_name = 'contribute.html'
    
    def get(self, request):
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
            user = authenticate(username=rq['email'], email=rq['email'], password=rq["password"])
            if user is not None:
                login(request, user)
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
            self.ctx = "Passwords do not match."
            if rq["password"] == rq["confirm-password"]:  
                self.ctx = "Password must be at least 8 characters."
                if len(rq["password"]) >= 8:
                    self.ctx = "Enter a valid email address."
                    if "@" in rq["email"]:
                        self.ctx = "Email already in use."
                        try:
                            user = User.objects.create_user(rq['email'], rq['email'], rq["password"])
                            user.save()
                        except:
                            return render(request, self.template_name, {'ctx': self.ctx})
                        user = authenticate(username=rq['email'], email=rq['email'], password=rq["password"])
                        if user is not None:
                            login(request, user)
                            return redirect('/contribute/')
        return render(request, self.template_name, {'ctx': self.ctx})