
from django.urls import path
from . import views
urlpatterns = [
    path('access/',views.access,name='access'),
    path('process/',views.predict_heart_disease,name='process'),
]