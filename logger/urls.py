from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignInPage.as_view(), name='signin'),
    path('page/',views.Page.as_view(), name='page')
]