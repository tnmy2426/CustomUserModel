from django.urls import path
from .import views

app_name = 'App_Register'

urlpatterns = [
    path('register/', views.RegisterView, name='register_view'),
    path('login/', views.LoginView, name='login_view'),
    path('logout/', views.LogoutView, name='logout_view'),
    path('email-confirmation/<str:activation_key>/', views.EmailConfirmation, name='email_confirmation'),

]
