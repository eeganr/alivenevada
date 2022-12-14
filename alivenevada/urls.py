"""alivenevada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web.views import ContributeView, LoginView, RegisterView, SuccessView
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from web.views import AnimalsView, PollutionView, InvasiveView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('contribute/', login_required(ContributeView.as_view())),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('animals/', login_required(AnimalsView.as_view())),
    path('pollution/', login_required(PollutionView.as_view())),
    path('invasive/', login_required(InvasiveView.as_view())),
    path('error/', TemplateView.as_view(template_name='error.html')),
    path('success/', SuccessView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
