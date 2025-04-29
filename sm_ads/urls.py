from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('index.html', views.main, name='main'),
    
    path('smp/<int:id>', views.socialMediaPlatform, name='detailPlatform'),
    path('cntr/<int:id>', views.countriesDetail, name='detailContry'),
    path('gnr/<int:id>', views.genderDetail, name='detailGender'),
    path('entr/<int:id>', views.entertainmentDetail, name='detailEntertainment'),
    path('', views.index, name='index'),
    path('api/users_by_country/', views.users_by_country, name='users_by_country'),
    path('api/devices_for_social_media/', views.devices_for_social_media, name='devices_for_social_media'),
    path('api/gender_distribution/', views.gender_distribution, name='gender_distribution'),
    path('occupations_main/', views.occupations_main, name='occupations_main'),
    path('summary-bubble-chart/', views.summary_bubble_chart, name='summary_bubble_chart'),
    

    #path('get_chart1/', views.get_chart1, name='get_chart1')
]
