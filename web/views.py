from django.shortcuts import render, redirect
from services.firebase import Firebase
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from web.forms import MapForm
from web.models import Place
from django.forms.models import model_to_dict
import os
from services.classification import TensorflowLiteClassificationModel

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
        print(Place.objects.all().values())
        return render(request, self.template_name, {'form': MapForm})

    def post(self, request):
        rq = request.POST.dict()
        form = MapForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            fb = Firebase()
            fb.login_token(request.session['fbtoken'])
            place.uuid = fb.user['userId']
            place.item = rq['animal_name']
            if 'wildfire' in rq:
                place.tf = True
            place.description = rq['notes']
            place.save()
            request.session['msg'] = ''
            if not place.item:
                model = TensorflowLiteClassificationModel(f"{os.getcwd()}/web/model.tflite", ['goldeneye', 'mink'])
                (label, probability) = model.run_from_filepath(f"{os.getcwd()}/media/{str(place.image)}")
                place.item = label[0]
                request.session['msg'] = f"Your image was classified as a {label[0]}."
            place.save()
            fb.storage.child('animals').child(str(place.image)[7:] + str(place.id)).put(f"{os.getcwd()}/media/{str(place.image)}", fb.user['idToken'])
            os.remove(f"{os.getcwd()}/media/{str(place.image)}")
            data = model_to_dict(place)
            data = {key: str(data[key]) for key in data.keys()}
            data['image'] = fb.storage.child('animals').child(str(place.image)[7:] + str(place.id)).get_url(fb.user['idToken'])
            fb.db.child('animals').push(data)
            return redirect('/success/')

        return render(request, self.template_name, {'form': MapForm})

class PollutionView(TemplateView):
    def __init__(self):
        self.template_name = 'pollution.html'
        self.ctx = ''

    def get(self, request):
        print(Place.objects.all().values())
        return render(request, self.template_name, {'form': MapForm})

    def post(self, request):
        rq = request.POST.dict()
        form = MapForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                place = form.save(commit=False)
                fb = Firebase()
                fb.login_token(request.session['fbtoken'])
                place.uuid = fb.user['userId']
                place.item = rq['pollution_name']
                place.save()
                fb.storage.child('pollution').child(str(place.image)[7:] + str(place.id)).put(f"{os.getcwd()}/media/{str(place.image)}", fb.user['idToken'])
                os.remove(f"{os.getcwd()}/media/{str(place.image)}")
                place.image = fb.storage.child('pollution').child(str(place.image)[7:] + str(place.id)).get_url(fb.user['idToken'])
                place.save()
                data = model_to_dict(place)
                data = {key: str(data[key]) for key in data.keys()}
                fb.db.child('pollution').push(data)
                request.session['msg'] = ''
                return redirect('/success/')
            except:
                return redirect('/error/')
        return render(request, self.template_name, {'form': MapForm})

class InvasiveView(TemplateView):
    def __init__(self):
        self.template_name = 'invasive.html'
        self.ctx = ''

    def get(self, request):
        print(Place.objects.all().values())
        return render(request, self.template_name, {'form': MapForm})

    def post(self, request):
        rq = request.POST.dict()
        print(rq)
        form = MapForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                place = form.save(commit=False)
                fb = Firebase()
                fb.login_token(request.session['fbtoken'])
                place.uuid = fb.user['userId']
                place.item = rq['invasive_name']
                place.description = rq['notes']
                place.save()
                fb.storage.child('invasive').child(str(place.image)[7:] + str(place.id)).put(f"{os.getcwd()}/media/{str(place.image)}", fb.user['idToken'])
                os.remove(f"{os.getcwd()}/media/{str(place.image)}")
                place.image = fb.storage.child('invasive').child(str(place.image)[7:] + str(place.id)).get_url(fb.user['idToken'])
                place.save()
                data = model_to_dict(place)
                data = {key: str(data[key]) for key in data.keys()}
                fb.db.child('invasive').push(data)
                request.session['msg'] = ''
                return redirect('/success/')
            except:
                return redirect('/error/')

        return render(request, self.template_name, {'form': MapForm})

class SuccessView(TemplateView):
    def __init__(self):
        self.template_name = 'success.html'
        self.ctx = ''

    def get(self, request):
        return render(request, self.template_name, {'msg': request.session['msg']})