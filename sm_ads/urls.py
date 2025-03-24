from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('index.html', views.main, name='main'),
    
    path('smp/<int:id>', views.socialMediaPlatform, name='detailPlatform'),
    path('cntr/<int:id>', views.countriesDetail, name='detailContry'),
    path('gnr/<int:id>', views.genderDetail, name='detailGender'),
    path('entr/<int:id>', views.entertainmentDetail, name='detailEntertainment'),
    
    path('general.html', views.general, name='general'),



    #path('get_chart1/', views.get_chart1, name='get_chart1')
]