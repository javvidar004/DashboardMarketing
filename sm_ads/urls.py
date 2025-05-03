from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('index.html', views.main, name='main'),
    
    path('smp/<int:id>', views.socialMediaPlatform, name='detailPlatform'),
    path('cntr/<int:id>', views.countriesDetail, name='detailContry'),
    path('gnr/<int:id>', views.genderDetail, name='detailGender'),
    path('entr/<int:id>', views.entertainmentDetail, name='detailEntertainment'),
    path('api/users_by_country/', views.users_by_country, name='users_by_country'),
    path('api/devices_for_social_media/', views.devices_for_social_media, name='devices_for_social_media'),
    path('api/gender_distribution/', views.gender_distribution, name='gender_distribution'),
    path('occupations_main/', views.occupations_main, name='occupations_main'),
    path('summary-bubble-chart/', views.summary_bubble_chart, name='summary_bubble_chart'),
    path('get_total_users/', views.get_total_users, name='get_total_users'),
    path('get_avg_age/', views.get_avg_age, name='get_avg_age'),
    path('get_top_social_media/', views.get_top_social_media, name='get_top_social_media'),
    
    path('get_avg_income/', views.get_avg_age, name='get_avg_income'),
    
    path('get_top_country/', views.get_top_country, name='get_top_country'),
    
    path('get_top_device/', views.get_top_device, name='get_top_device'),
    
    path('smp/<int:id>', views.socialMediaPlatform, name='detailPlatform'), # Esta ya la tenías

    # --- API URLs for Social Media Platform Details ---
    path('api/smp/<int:platform_id>/age_distribution/', views.smp_age_distribution, name='smp_age_distribution'),
    path('api/smp/<int:platform_id>/gender_distribution/', views.smp_gender_distribution, name='smp_gender_distribution'),
    path('api/smp/<int:platform_id>/top_countries/', views.smp_top_countries, name='smp_top_countries'),
    path('api/smp/<int:platform_id>/top_occupations/', views.smp_top_occupations, name='smp_top_occupations'),
    
    path('cntr/<int:id>', views.countriesDetail, name='detailContry'), # Esta ya la tenías

    # --- API URLs for Country Details ---
    path('api/country/<int:country_id>/age_distribution/', views.country_age_distribution, name='country_age_distribution'),
    path('api/country/<int:country_id>/gender_distribution/', views.country_gender_distribution, name='country_gender_distribution'),
    path('api/country/<int:country_id>/top_platforms/', views.country_top_platforms, name='country_top_platforms'),
    path('api/country/<int:country_id>/top_entertainment/', views.country_top_entertainment, name='country_top_entertainment'),
    path('api/country/<int:country_id>/sm_vs_ent_time/', views.country_sm_vs_ent_time, name='country_sm_vs_ent_time'),
    path('api/country/<int:country_id>/income_spending/', views.country_income_spending, name='country_income_spending'),
    
    path('gnr/<int:id>', views.genderDetail, name='detailGender'), # Esta ya la tenías

    # --- API URLs for Gender Details ---
    path('api/gender/<int:gender_id>/age_distribution/', views.gender_age_distribution, name='gender_age_distribution'),
    path('api/gender/<int:gender_id>/top_platforms/', views.gender_top_platforms, name='gender_top_platforms'),
    path('api/gender/<int:gender_id>/top_entertainment/', views.gender_top_entertainment, name='gender_top_entertainment'),
    path('api/gender/<int:gender_id>/top_occupations/', views.gender_top_occupations, name='gender_top_occupations'),
    path('api/gender/<int:gender_id>/sm_vs_ent_time/', views.gender_sm_vs_ent_time, name='gender_sm_vs_ent_time'),
    path('api/gender/<int:gender_id>/income_spending/', views.gender_income_spending, name='gender_income_spending'),
    
    path('entr/<int:id>', views.entertainmentDetail, name='detailEntertainment'), # Esta ya la tenías

    # --- API URLs for Entertainment Type Details ---
    path('api/entertainment/<int:entertainment_id>/age_distribution/', views.ent_age_distribution, name='ent_age_distribution'),
    path('api/entertainment/<int:entertainment_id>/gender_distribution/', views.ent_gender_distribution, name='ent_gender_distribution'),
    path('api/entertainment/<int:entertainment_id>/top_countries/', views.ent_top_countries, name='ent_top_countries'),
    path('api/entertainment/<int:entertainment_id>/top_platforms/', views.ent_top_platforms, name='ent_top_platforms'),
    path('api/entertainment/<int:entertainment_id>/top_occupations/', views.ent_top_occupations, name='ent_top_occupations'),
    path('api/entertainment/<int:entertainment_id>/device_usage/', views.ent_device_usage, name='ent_device_usage'),

]
    

    #path('get_chart1/', views.get_chart1, name='get_chart1')

