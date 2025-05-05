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
    
    path('api/smp/<int:platform_id>/age_gender_distribution/', views.smp_age_gender_distribution, name='smp_age_gender_distribution'),
    path('api/smp/<int:platform_id>/occupation_income/', views.smp_occupation_income_profile, name='smp_occupation_income'),
    path('api/smp/<int:platform_id>/content_affinity/', views.smp_content_affinity, name='smp_content_affinity'),
    path('api/smp/<int:platform_id>/user_intent/', views.smp_user_intent, name='smp_user_intent'),
    path('api/smp/<int:platform_id>/engagement_spending/', views.smp_engagement_spending_profile, name='smp_engagement_spending'),
    path('api/smp/<int:platform_id>/device_profile/', views.smp_device_profile, name='smp_device_profile'),

    # --- APIs que ya tenías y podrías mantener/reutilizar si quieres ---
    path('api/smp/<int:platform_id>/top_countries/', views.smp_top_countries, name='smp_top_countries'), # Reutilizamos la de países
    
    path('api/country/<int:country_id>/income_distribution/', views.country_income_distribution, name='country_income_distribution'),
    path('api/country/<int:country_id>/spending_distribution/', views.country_spending_distribution, name='country_spending_distribution'),
    path('api/country/<int:country_id>/occupation_landscape/', views.country_occupation_landscape, name='country_occupation_landscape'),
    #path('api/country/<int:country_id>/time_allocation/', views.country_time_allocation, name='country_time_allocation'),
    path('api/country/<int:country_id>/lifestyle_indicators/', views.country_lifestyle_indicators, name='country_lifestyle_indicators'),
    #path('api/country/<int:country_id>/age_gender_mix/', views.country_age_gender_mix, name='country_age_gender_mix'), # Nueva o reutilizada
    path('api/country/<int:country_id>/tech_savviness_distribution/', views.country_tech_savviness_distribution, name='country_tech_savviness_distribution'), # NUEVA


    # --- APIs que ya tenías y puedes reutilizar ---
    path('api/country/<int:country_id>/top_platforms/', views.country_top_platforms, name='country_top_platforms'),
    path('api/country/<int:country_id>/top_entertainment/', views.country_top_entertainment, name='country_top_entertainment'),
    
    path('api/gender/<int:gender_id>/platform_preference/', views.gender_platform_preference, name='gender_platform_preference'),
    path('api/gender/<int:gender_id>/income_vs_spending/', views.gender_income_vs_spending, name='gender_income_vs_spending'),
    path('api/gender/<int:gender_id>/sm_goal_distribution/', views.gender_sm_goal_distribution, name='gender_sm_goal_distribution'),
    path('api/gender/<int:gender_id>/engagement_indicators/', views.gender_engagement_indicators, name='gender_engagement_indicators'),

    # --- APIs Reutilizadas/Existentes ---
    path('api/gender/<int:gender_id>/top_entertainment/', views.gender_top_entertainment, name='gender_top_entertainment'),
    path('api/gender/<int:gender_id>/sm_vs_ent_time/', views.gender_sm_vs_ent_time, name='gender_sm_vs_ent_time'),
    path('api/gender/<int:gender_id>/top_occupations/', views.gender_top_occupations, name='gender_top_occupations'),
    # Mantén la de age_distribution si quieres un gráfico demográfico simple, o elimínala
    path('api/gender/<int:gender_id>/age_distribution/', views.gender_age_distribution, name='gender_age_distribution'),
    
    path('api/entertainment/<int:entertainment_id>/core_demographics/', views.ent_core_demographics, name='ent_core_demographics'),
    path('api/entertainment/<int:entertainment_id>/socioeconomic_profile/', views.ent_socioeconomic_profile, name='ent_socioeconomic_profile'),
    path('api/entertainment/<int:entertainment_id>/platform_and_device/', views.ent_platform_and_device, name='ent_platform_and_device'),
    path('api/entertainment/<int:entertainment_id>/engagement_profile/', views.ent_engagement_profile, name='ent_engagement_profile'),

    path('smp/<int:id>/', views.socialMediaPlatform, name='detailPlatform'), # Añadir / al final
    path('cntr/<int:id>/', views.countriesDetail, name='detailContry'),   # Añadir / al final
    path('gnr/<int:id>/', views.genderDetail, name='detailGender'),       # Añadir / al final
    path('entr/<int:id>/', views.entertainmentDetail, name='detailEntertainment'), # Añadir / al final

    # --- APIs para el NUEVO Dashboard Principal (index.html) ---
    path('api/main/top_platforms/', views.get_top_platforms_distribution, name='main_top_platforms'),
    path('api/main/top_entertainment/', views.get_top_entertainment_distribution, name='main_top_entertainment'),
    path('api/main/users_by_country/', views.get_users_by_country_distribution, name='main_users_by_country'),
    path('api/main/platform_highest_income/', views.get_platform_highest_avg_income, name='main_platform_highest_income'),
    path('api/main/platform_highest_savvy/', views.get_platform_for_highest_tech_savvy, name='main_platform_highest_savvy'),
    path('api/main/subs_per_income/', views.get_avg_subscriptions_per_income_bracket, name='main_subs_per_income'),
    path('api/main/sleep_by_notifications/', views.get_sleep_quality_by_notification_level, name='main_sleep_by_notifications'),
    path('api/main/sm_time_by_gaming/', views.get_sm_time_by_gaming_level, name='main_sm_time_by_gaming'),
    path('api/main/age_ad_interaction/', views.get_age_group_highest_ad_interaction, name='main_age_ad_interaction'),
    path('api/main/occupation_distinct_ent/', views.get_occupation_distinct_entertainment, name='main_occupation_distinct_ent'),
    path('api/main/country_highest_screen/', views.get_country_highest_screen_time, name='main_country_highest_screen'),
]
    

    #path('get_chart1/', views.get_chart1, name='get_chart1')

