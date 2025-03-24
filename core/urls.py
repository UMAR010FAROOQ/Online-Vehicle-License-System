from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'core'

urlpatterns = [
    path('', views.HomePage, name="HomePage"),
    path('LearningMaterial', views.LearningMaterialPage, name="LearningMaterialPage"),
    path('FeeStructure', views.FeeStructurePage, name="FeeStructurePage"),
    path('SampleTest', views.SampleTestPage, name="SampleTestPage"),
    path('TrackApplication', views.TrackApplicationPage, name="TrackApplicationPage"),
    path('VerifyLicense', views.VerifyLicensePage, name="VerifyLicensePage"),
    path('LearnerApplication', views.LearnerApplicationPage, name="LearnerApplicationPage"),
    path('LearnerApply', views.LearnerApplyPage, name="LearnerApplyPage"),
    path('success/', views.SuccessPage, name='success_page'),


    path("user_registration", views.user_registration, name="user_registration"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path('reset_password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('change_password/', change_password, name='change_password'),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
