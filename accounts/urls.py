from django.urls import path
from .views import registration_view, logout_view, login_view, user_data_change_view

urlpatterns = [
    path('register', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('change/', user_data_change_view, name='change'),
]
