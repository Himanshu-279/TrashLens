from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('about/', views.about_view, name='about'),
    path('classifier/', views.classifier_view, name='classifier'),
    path('waste-types/', views.waste_types_view, name='waste_types'),
    path('dos-and-donts/', views.dos_and_donts_view, name='dos_and_donts'),
    path('result/', views.result_view, name='result'),
    path('feedback/', views.map_feedback_view, name='map_feedback'),
    path('download/', views.download_app_page, name='download_app'),
]