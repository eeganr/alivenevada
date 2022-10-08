from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

class ContributeView(TemplateView):
    def __init__(self):
        self.template_name = 'contribute.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)

class LoginView(TemplateView):
    def __init__(self):
        self.template_name = 'login.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)

class RegisterView(TemplateView):
    def __init__(self):
        self.template_name = 'register.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)