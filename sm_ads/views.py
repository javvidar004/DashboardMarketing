from django.http import HttpResponse
from django.template import loader
from .models import SocialMedia

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
from random import randrange
from .models import *

from django.shortcuts import render
from django.db import connection

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from .models import Users, Countries, Devices, SocialMedia, MediaGoal, Entretaiment, Gender

def auxMenu():
  redesSociales = SocialMedia.objects.all().values()
  paises = Countries.objects.all().values()
  generos = Gender.objects.all().values()
  tipoEntretenimiento = Entretaiment.objects.all().values()
  return redesSociales, paises, generos, tipoEntretenimiento

def main(request):
  #consumo por tipo de entretenimiento
    prefEntre = Entretaiment.objects.raw(f'''SELECT entretaiment.entertainment_id AS entertainment_id, entretaiment.entertainment_name AS name, COUNT(preferred_content_id) AS people 
                                        FROM entretaiment, users 
                                        WHERE preferred_content_id = entretaiment.entertainment_id 
                                        GROUP BY entretaiment.entertainment_id;''')
    #orden por pais que mas gasta en entretenimiento
    spentEntre = Countries.objects.raw(f'''SELECT countries.country_id, countries.country_name, ROUND(SUM(users.monthly_spent_entertain),2) AS total_spent
                                            FROM users
                                            JOIN countries ON users.country_id = countries.country_id
                                            GROUP BY countries.country_id, countries.country_name
                                            ORDER BY total_spent DESC;''')
        #orden por pais con mayor promedio
    gainsPais = Countries.objects.raw(f'''SELECT countries.country_id, countries.country_name, ROUND(AVG(users.monthly_income),2) AS avg_income
                                            FROM users
                                            JOIN countries ON users.country_id = countries.country_id
                                            GROUP BY countries.country_id, countries.country_name
                                            ORDER BY avg_income DESC;''')
    edadRsPais = Countries.objects.raw(f'''SELECT countries.country_id, countries.country_name, social_media.socialm_name AS Platform,
                                            CASE 
                                            WHEN users.age BETWEEN 0 AND 17 THEN '0-17'
                                            WHEN users.age BETWEEN 18 AND 25 THEN '18-25'
                                            WHEN users.age BETWEEN 26 AND 35 THEN '26-35'
                                            WHEN users.age BETWEEN 36 AND 50 THEN '36-50'
                                            ELSE '51+' 
                                            END AS age_group,
                                            COUNT(*) AS total_users
                                            FROM users
                                            JOIN countries ON users.country_id = countries.country_id
                                            JOIN social_media ON users.primary_plat_id = social_media.socialm_id
                                            GROUP BY countries.country_name, social_media.socialm_name, age_group, countries.country_id
                                            ORDER BY countries.country_name, social_media.socialm_name, total_users DESC;''')
    gastoOcupacion = Occupations.objects.raw('''SELECT occupations.occupation_id, occupations.occupation_name, ROUND(SUM(users.monthly_spent_entertain),2) AS total_spent
                                            FROM users
                                            JOIN occupations ON users.occupation_id = occupations.occupation_id
                                            GROUP BY occupations.occupation_name, occupations.occupation_id
                                            ORDER BY total_spent DESC;''')
    objetivoOcupacion = Occupations.objects.raw('''SELECT occupations.occupation_name, media_goal.goal_name, COUNT(*) AS total_users
                                            FROM users
                                            JOIN occupations ON users.occupation_id = occupations.occupation_id
                                            JOIN media_goal ON users.primary_sm_goal_id = media_goal.goal_id
                                            GROUP BY occupations.occupation_name, media_goal.goal_name
                                            ORDER BY occupations.occupation_name, total_users DESC;''')
    dispositivosConsumEntr = Occupations.objects.raw('''SELECT 
                                            devices.device_name,
                                            COUNT(*) AS total_users
                                            FROM users
                                            JOIN devices ON users.device_sm_id = devices.device_id
                                            GROUP BY devices.device_name
                                            ORDER BY total_users DESC;''')
    dispositivosConsumRS = Occupations.objects.raw('''SELECT 
                                            devices.device_name,
                                            COUNT(*) AS total_users
                                            FROM users
                                            JOIN devices ON users.devide_for_entertainment_id = devices.device_id
                                            GROUP BY devices.device_name
                                            ORDER BY total_users DESC;''')
    relacioningresos_gastos_entr = Occupations.objects.raw('''SELECT country_name, AVG(users.monthly_income) AS prom_ingresos, AVG(users.monthly_spent_entertain) AS prom_gastos
                                            FROM users
                                            JOIN countries ON users.country_id = countries.country_id
                                            GROUP BY country_name
                                            ORDER BY prom_gastos DESC;''')
    paises_rs_vs_entr = Occupations.objects.raw('''SELECT countries.country_name, AVG(users.d_sm_time) AS prom_redes_sociales, AVG(users.d_entertain_time) AS prom_plat_entret
                                            FROM users
                                            JOIN countries ON users.country_id = countries.country_id
                                            GROUP BY countries.country_name
                                            ORDER BY prom_redes_sociales DESC;''')
    rs_uso_ocupacion = Occupations.objects.raw('''SELECT occupations.occupation_name, social_media.socialm_name,
                                            COUNT(users.user_id) AS total_usuarios
                                            FROM users
                                            JOIN occupations ON users.occupation_id = occupations.occupation_id
                                            JOIN social_media ON users.primary_plat_id = social_media.socialm_id
                                            GROUP BY occupations.occupation_name, social_media.socialm_name
                                            ORDER BY total_usuarios DESC;''')
    suegno_vs_tiempopant = Occupations.objects.raw('''SELECT 
                                            CASE 
                                                WHEN screen_time < 3 THEN 'Bajo'
                                                WHEN screen_time BETWEEN 3 AND 6 THEN 'Moderado'
                                                ELSE 'Alto'
                                            END AS screen_usage,
                                            CASE 
                                                WHEN sleep_quality >= 7 THEN 'Buena'
                                                WHEN sleep_quality BETWEEN 5 AND 6 THEN 'Regular'
                                                ELSE 'Mala'
                                            END AS sleep_category,
                                            COUNT(*) AS users_count
                                            FROM users
                                            GROUP BY screen_usage, sleep_category
                                            ORDER BY users_count DESC;''')
    

    #   dispositivosConsumEntr = Occupations.objects.raw('''''')
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('index.html') 
    context = {
        'prefEntre' : prefEntre,
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento,
        'spentEntre': spentEntre,
        'gainsPais': gainsPais,
        'edadRsPais':edadRsPais,
        'gastoOcupacion':gastoOcupacion,
        'objetivoOcupacion': objetivoOcupacion,
        'dispositivosConsumEntr' : dispositivosConsumEntr,
        'dispositivosConsumRS' : dispositivosConsumRS,
        'relacioningresos_gastos_entr' : relacioningresos_gastos_entr,
        'paises_rs_vs_entr' : paises_rs_vs_entr,
        'rs_uso_ocupacion' : rs_uso_ocupacion,
        'suegno_vs_tiempopant' : suegno_vs_tiempopant
    }
    return HttpResponse(template.render(context, request))

  #path('smp/<int:id>', views.socialMediaPlatform, name=detailPlatform)
def socialMediaPlatform(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('smp.html')
    titulo = ''
    for i in redesSociales:
       if id == i['socialm_id']:
          titulo = i['socialm_name']
    context = {
     'redesSociales': redesSociales,
     'paises': paises,
     'generos': generos,
     'tipoEntretenimiento': tipoEntretenimiento,
     'titulo': titulo.upper(),
    }
    return HttpResponse(template.render(context, request))
  
  #path('cntr/<int:id>', views.countriesDetail, name=detailContry)
def countriesDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('paises.html')
    titulo = ''
    for i in paises:
       if id == i['country_id']:
          titulo = i['country_name']
    context = {
      'redesSociales': redesSociales,
      'paises': paises,
      'generos': generos,
      'tipoEntretenimiento': tipoEntretenimiento,
      'titulo': titulo.upper(),
    }
    return HttpResponse(template.render(context, request))

  #path('gnr/<int:id>', views.genderDetail, name=detailGender)
def genderDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('generos.html')
    titulo = ''
    for i in generos:
       if id == i['gender_id']:
          titulo = i['gender']
    context = {
       'redesSociales': redesSociales,
       'paises': paises,
       'generos': generos,
       'tipoEntretenimiento': tipoEntretenimiento,
       'titulo': titulo.upper(),
    }
    return HttpResponse(template.render(context, request))

  #path('entr/<int:id>', views.entertainmentDetail, name=detailEntertainment)
def entertainmentDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('entretenimiento.html')
    titulo = ''
    for i in tipoEntretenimiento:
       if id == i['entertainment_id']:
          titulo = i['entertainment_name']
    context = {
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento,
        'titulo': titulo.upper(),
    }
    return HttpResponse(template.render(context, request))

def index(request):
    return render(request, 'index.html')


def users_by_country(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.country_name, COUNT(u.user_id) AS total
            FROM users u
            JOIN countries c ON u.country_id = c.country_id
            GROUP BY c.country_name
            ORDER BY total DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()

    data = {
        'labels': [row[0] for row in rows],
        'data': [row[1] for row in rows]
    }
    return JsonResponse(data)


def devices_for_social_media(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.device_name, COUNT(u.user_id) AS total
            FROM users u
            JOIN devices d ON u.device_sm_id = d.device_id
            GROUP BY d.device_name
            ORDER BY total DESC
        """)
        rows = cursor.fetchall()

    data = {
        'labels': [row[0] for row in rows],
        'data': [row[1] for row in rows]
    }
    return JsonResponse(data)

def gender_distribution(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.gender, COUNT(u.user_id) AS total
            FROM users u
            JOIN gender g ON u.gender_id = g.gender_id
            GROUP BY g.gender
        """)
        rows = cursor.fetchall()

    data = {
        'labels': [row[0] for row in rows],
        'data': [row[1] for row in rows]
    }
    return JsonResponse(data)

def top_occupations(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.occupation_name, COUNT(u.user_id) AS total
            FROM users u
            JOIN occupations o ON u.occupation_id = o.occupation_id
            GROUP BY o.occupation_name
            ORDER BY total DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()

    data = {
        'labels': [row[0] for row in rows],
        'data': [row[1] for row in rows]
    }
    return JsonResponse(data)

def occupations_main(request):
    query = """
        SELECT o.occupation_name, COUNT(u.user_id) as total
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        GROUP BY o.occupation_name
        ORDER BY total DESC
        LIMIT 10
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    labels = [row[0] for row in rows]
    data = [row[1] for row in rows]

    return JsonResponse({'labels': labels, 'data': data})

def summary_bubble_chart(request):
    query = """
        SELECT 
            o.occupation_name, 
            c.country_name, 
            u.tech_savviness_level, 
            ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
            COUNT(u.user_id) as user_count
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        JOIN countries c ON u.country_id = c.country_id
        WHERE u.tech_savviness_level IS NOT NULL AND u.d_sm_time IS NOT NULL
        GROUP BY o.occupation_name, c.country_name, u.tech_savviness_level
        HAVING COUNT(u.user_id) > 5
        ORDER BY user_count DESC
        LIMIT 30
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    data = [{
        "x": row[2],  # tech_savviness_level
        "y": row[3],  # avg d_sm_time
        "r": row[4] / 2,  # user count scaled
        "label": f"{row[0]} - {row[1]}"  # occupation - country
    } for row in rows]

    return JsonResponse({"datasets": [{
        "label": "Usuarios por ocupación, país y nivel tecnológico",
        "data": data,
        "backgroundColor": "rgba(52, 152, 219, 0.7)",
        "borderColor": "#2980b9",
        "borderWidth": 1
    }]})


'''
def get_chart1(_request):

    colors = ['blue', 'orange', 'red', 'black', 'yellow', 'green', 'magenta', 'lightblue', 'purple', 'brown']
    random_color = colors[randrange(0, (len(colors)-1))]

    serie = []
    counter = 0

    while (counter < 7):
        serie.append(randrange(100, 400))
        counter += 1

    chart = {
        'tooltip': {
            'show': True,
            'trigger': "axis",
            'triggerOn': "mousemove|click"
        },
        'xAxis': [
            {
                'type': "category",
                'data': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            }
        ],
        'yAxis': [
            {
                'type': "value"
            }
        ],
        'series': [
            {
                'data': serie,
                'type': "line",
                'itemStyle': {
                    'color': random_color
                },
                'lineStyle': {
                    'color': random_color
                }
            }
        ]
    }

    return JsonResponse(chart)
'''

# Create your views here.