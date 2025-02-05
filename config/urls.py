"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render

from rag.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('survey/', survey_interface, name='survey_interface'),
    path('chatbot/', chatbot_interface, name='chatbot_interface'),
    path('generate-id/', generate_id, name='generate_custom_id'),
    path('get-questions/', get_questions, name='get_questions'),
    path('submit-response/', submit_response, name='submit_response'),
    path('ask-openai/', ask_openai, name='ask_openai')
]
