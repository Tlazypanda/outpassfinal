from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('request/list', views.all_requests, name='all_requests'),
    path('request/<int:pk>/', views.request_detail, name='request_detail'),
    path('request/new/', views.request_new, name='request_new'),
    path('request/<int:pk>/edit/', views.request_edit, name='request_edit'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]
