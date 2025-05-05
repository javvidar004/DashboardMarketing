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
from .models import Users, Countries, Devices, SocialMedia, MediaGoal, Entretaiment, Gender, Occupations

def auxMenu():
    redesSociales = SocialMedia.objects.all().values()
    paises = Countries.objects.all().values()
    generos = Gender.objects.all().values()
    tipoEntretenimiento = Entretaiment.objects.all().values()
    return redesSociales, paises, generos, tipoEntretenimiento

def main(request):
    prefEntre = Entretaiment.objects.raw(f'''SELECT entretaiment.entertainment_id AS entertainment_id, entretaiment.entertainment_name AS name, COUNT(preferred_content_id) AS people
                                         FROM entretaiment, users
                                         WHERE preferred_content_id = entretaiment.entertainment_id
                                         GROUP BY entretaiment.entertainment_id;''')
    spentEntre = Countries.objects.raw(f'''SELECT countries.country_id, countries.country_name, ROUND(SUM(users.monthly_spent_entertain),2) AS total_spent
                                         FROM users
                                         JOIN countries ON users.country_id = countries.country_id
                                         GROUP BY countries.country_id, countries.country_name
                                         ORDER BY total_spent DESC;''')
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
    total_users_entr = Users.objects.raw('''SELECT COUNT(*) AS total_users FROM users;''')


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
        'suegno_vs_tiempopant' : suegno_vs_tiempopant,
        'total_users_entr' : get_total_users_count(),
        'avg_age': get_avg_age_value(),
        'top_social_media': get_top_social_media(),
        'avg_income': get_avg_income_value(),
        'top_country': get_top_country(),
        'top_device': get_top_device(),
    }
    return HttpResponse(template.render(context, request))

def redsocial(request, id):
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
        "x": row[2],
        "y": row[3],
        "r": row[4] / 2,
        "label": f"{row[0]} - {row[1]}"
    } for row in rows]

    return JsonResponse({"datasets": [{
        "label": "Usuarios por ocupación, país y nivel tecnológico",
        "data": data,
        "backgroundColor": "rgba(52, 152, 219, 0.7)",
        "borderColor": "#2980b9",
        "borderWidth": 1
    }]})

def get_total_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users;")
        return cursor.fetchone()[0]


def get_avg_age():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ROUND(AVG(age), 1) FROM users;")
        return cursor.fetchone()[0]

def get_top_social_media():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT primary_plat_id
            FROM users
            GROUP BY primary_plat_id
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result[0] if result else "N/A"

def get_avg_income():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ROUND(AVG(monthly_income), 2) FROM users;")
        return cursor.fetchone()[0]

def get_top_country():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT country_id
            FROM users
            GROUP BY country_id
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result[0] if result else "N/A"

def get_top_device():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT device_sm_id
            FROM users
            GROUP BY device_sm_id
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result[0] if result else "N/A"

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def execute_query(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return dictfetchall(cursor)
            else:
                result = cursor.fetchone()
                if result and cursor.description:
                    cursor.execute(query, params)
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, result))]
                elif result:
                    return [{'result': result[0]}]
                else:
                    return []
    except Exception as e:
        print(f"ERROR ejecutando query: {e}\nQuery: {query}\nParams: {params}")
        return []


def smp_age_distribution(request, platform_id):
    query = """
        SELECT
            CASE
                WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
                WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
                WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
                WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            COUNT(u.user_id) AS total_users
        FROM users u
        WHERE u.primary_plat_id = %s
        GROUP BY age_group
        ORDER BY age_group;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list):
        data = []

    chart_data = {
        'labels': [row.get('age_group', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip()
    }
    return JsonResponse(chart_data)

def smp_gender_distribution(request, platform_id):
    query = """
        SELECT
            g.gender,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.primary_plat_id = %s
        GROUP BY g.gender
        ORDER BY total_users DESC;
    """
    data = execute_query(query, [platform_id])

    if not isinstance(data, list):
        data = []

    chart_data = {
        'labels': [row.get('gender', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip()
    }
    return JsonResponse(chart_data)

def smp_top_countries(request, platform_id):
    query = """
        SELECT
            c.country_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN countries c ON u.country_id = c.country_id
        WHERE u.primary_plat_id = %s
        GROUP BY c.country_name
        ORDER BY total_users DESC
        LIMIT 10;
    """
    data = execute_query(query, [platform_id])

    if not isinstance(data, list):
        data = []

    chart_data = {
        'labels': [row.get('country_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip()
    }
    return JsonResponse(chart_data)

def smp_top_occupations(request, platform_id):
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.primary_plat_id = %s
        GROUP BY o.occupation_name
        ORDER BY total_users DESC
        LIMIT 10;
    """
    data = execute_query(query, [platform_id])

    if not isinstance(data, list):
        data = []

    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip()
    }
    return JsonResponse(chart_data)

def redsocial(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('smp.html')
    titulo = ''
    platform_name = 'Plataforma Desconocida'
    try:
        platform = SocialMedia.objects.get(pk=id)
        platform_name = platform.socialm_name
        titulo = platform_name.upper()
    except SocialMedia.DoesNotExist:
        pass

    context = {
     'redesSociales': redesSociales,
     'paises': paises,
     'generos': generos,
     'tipoEntretenimiento': tipoEntretenimiento,
     'titulo': titulo,
     'platform_name': platform_name,
     'platform_id': id,
    }
    return HttpResponse(template.render(context, request))

def country_age_distribution(request, country_id):
    query = """
        SELECT
            CASE
                WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
                WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
                WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
                WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            COUNT(u.user_id) AS total_users
        FROM users u
        WHERE u.country_id = %s
        GROUP BY age_group
        ORDER BY age_group;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('age_group', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_gender_distribution(request, country_id):
    query = """
        SELECT
            g.gender,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.country_id = %s
        GROUP BY g.gender
        ORDER BY total_users DESC;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('gender', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_top_platforms(request, country_id):
    query = """
        SELECT
            sm.socialm_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.country_id = %s
        GROUP BY sm.socialm_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('socialm_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_top_entertainment(request, country_id):
    query = """
        SELECT
            e.entertainment_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
        WHERE u.country_id = %s
        GROUP BY e.entertainment_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('entertainment_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_sm_vs_ent_time(request, country_id):
    query = """
        SELECT
            ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
            ROUND(AVG(u.d_entertain_time), 2) AS avg_ent_time
        FROM users u
        WHERE u.country_id = %s;
    """
    data = execute_query(query, [country_id])

    result = {}
    if isinstance(data, dict):
        result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'],
                  'data': [data.get('avg_sm_time', 0), data.get('avg_ent_time', 0)] }
    elif isinstance(data, (list, tuple)) and len(data) >= 2:
          result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'],
                    'data': [data[0] if data[0] is not None else 0, data[1] if data[1] is not None else 0]}
    else:
        result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'], 'data': [0, 0]}


    return JsonResponse(result)


def country_income_spending(request, country_id):
    query = """
        SELECT
            ROUND(AVG(u.monthly_income), 2) AS avg_income,
            ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spent
        FROM users u
        WHERE u.country_id = %s;
    """
    data = execute_query(query, [country_id])
    result = {}
    if isinstance(data, dict):
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'],
                    'data': [data.get('avg_income', 0), data.get('avg_spent', 0)]}
    elif isinstance(data, (list, tuple)) and len(data) >= 2:
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'],
                    'data': [data[0] if data[0] is not None else 0, data[1] if data[1] is not None else 0]}
    else:
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'], 'data': [0, 0]}

    return JsonResponse(result)

def countriesDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('paises.html')
    titulo = ''
    country_name = 'País Desconocido'
    try:
        country = Countries.objects.get(pk=id)
        country_name = country.country_name
        titulo = country_name.upper()
    except Countries.DoesNotExist:
        pass

    context = {
      'redesSociales': redesSociales,
      'paises': paises,
      'generos': generos,
      'tipoEntretenimiento': tipoEntretenimiento,
      'titulo': titulo,
      'country_name': country_name,
      'country_id': id,
    }
    return HttpResponse(template.render(context, request))

def gender_age_distribution(request, gender_id):
    query = """
        SELECT
            CASE
                WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
                WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
                WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
                WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            COUNT(u.user_id) AS total_users
        FROM users u
        WHERE u.gender_id = %s
        GROUP BY age_group
        ORDER BY age_group;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('age_group', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def gender_top_platforms(request, gender_id):
    query = """
        SELECT
            sm.socialm_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.gender_id = %s
        GROUP BY sm.socialm_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('socialm_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def gender_top_entertainment(request, gender_id):
    query = """
        SELECT
            e.entertainment_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
        WHERE u.gender_id = %s
        GROUP BY e.entertainment_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('entertainment_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def gender_top_occupations(request, gender_id):
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.gender_id = %s
        GROUP BY o.occupation_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def gender_sm_vs_ent_time(request, gender_id):
    query = """
        SELECT
            ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
            ROUND(AVG(u.d_entertain_time), 2) AS avg_ent_time
        FROM users u
        WHERE u.gender_id = %s;
    """
    data = execute_query(query, [gender_id])
    result = {}
    if isinstance(data, dict):
        result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'],
                  'data': [data.get('avg_sm_time', 0), data.get('avg_ent_time', 0)] }
    elif isinstance(data, (list, tuple)) and len(data) >= 2:
          result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'],
                    'data': [data[0] if data[0] is not None else 0, data[1] if data[1] is not None else 0]}
    else:
        result = {'labels': ['Tiempo en Redes Sociales', 'Tiempo en Entretenimiento'], 'data': [0, 0]}
    return JsonResponse(result)

def gender_income_spending(request, gender_id):
    query = """
        SELECT
            ROUND(AVG(u.monthly_income), 2) AS avg_income,
            ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spent
        FROM users u
        WHERE u.gender_id = %s;
    """
    data = execute_query(query, [gender_id])
    result = {}
    if isinstance(data, dict):
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'],
                    'data': [data.get('avg_income', 0), data.get('avg_spent', 0)]}
    elif isinstance(data, (list, tuple)) and len(data) >= 2:
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'],
                    'data': [data[0] if data[0] is not None else 0, data[1] if data[1] is not None else 0]}
    else:
          result = {'labels': ['Ingreso Promedio Mensual', 'Gasto Promedio Entretenimiento'], 'data': [0, 0]}
    return JsonResponse(result)


def genderDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('generos.html')
    titulo = ''
    gender_name = 'Género Desconocido'
    try:
        gender_obj = Gender.objects.get(pk=id)
        gender_name = gender_obj.gender
        titulo = gender_name.upper()
    except Gender.DoesNotExist:
        pass

    context = {
       'redesSociales': redesSociales,
       'paises': paises,
       'generos': generos,
       'tipoEntretenimiento': tipoEntretenimiento,
       'titulo': titulo,
       'gender_name': gender_name,
       'gender_id': id,
    }
    return HttpResponse(template.render(context, request))

def ent_age_distribution(request, entertainment_id):
    query = """
        SELECT
            CASE
                WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
                WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
                WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
                WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            COUNT(u.user_id) AS total_users
        FROM users u
        WHERE u.preferred_content_id = %s
        GROUP BY age_group
        ORDER BY age_group;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('age_group', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def ent_gender_distribution(request, entertainment_id):
    query = """
        SELECT
            g.gender,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.preferred_content_id = %s
        GROUP BY g.gender
        ORDER BY total_users DESC;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('gender', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def ent_top_countries(request, entertainment_id):
    query = """
        SELECT
            c.country_name,
            COUNT(u.user_id) AS people
        FROM users u
        JOIN countries c ON u.country_id = c.country_id
        WHERE u.preferred_content_id = %s
        GROUP BY c.country_name
        ORDER BY people DESC
        LIMIT 5;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('country_name', 'N/A') for row in data],
        'data': [row.get('people', 0) for row in data],
    }
    return JsonResponse(chart_data)

def ent_top_platforms(request, entertainment_id):
    query = """
        SELECT
            sm.socialm_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.preferred_content_id = %s
        GROUP BY sm.socialm_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('socialm_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def ent_top_occupations(request, entertainment_id):
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.preferred_content_id = %s
        GROUP BY o.occupation_name
        ORDER BY total_users DESC
        LIMIT 5;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def ent_device_usage(request, entertainment_id):
    query = """
        SELECT
            d.device_name,
            COUNT(u.user_id) AS total_users
        FROM users u
        JOIN devices d ON u.devide_for_entertainment_id = d.device_id
        WHERE u.preferred_content_id = %s
        GROUP BY d.device_name
        ORDER BY total_users DESC;
    """
    data = execute_query(query, [entertainment_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('device_name', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
    }
    return JsonResponse(chart_data)

def entertainmentDetail(request, id):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('entretenimiento.html')
    titulo = ''
    entertainment_name = 'Tipo Desconocido'
    try:
        entertainment_obj = Entretaiment.objects.get(pk=id)
        entertainment_name = entertainment_obj.entertainment_name
        titulo = entertainment_name.upper()
    except Entretaiment.DoesNotExist:
        pass

    context = {
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento,
        'titulo': titulo,
        'entertainment_name': entertainment_name,
        'entertainment_id': id,
    }
    return HttpResponse(template.render(context, request))


def smp_age_gender_distribution(request, platform_id):
    query = """
        SELECT
            CASE
                WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
                WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
                WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
                WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            g.gender,
            COUNT(u.user_id) AS count
        FROM users u
        JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.primary_plat_id = %s
        GROUP BY age_group, g.gender
        ORDER BY age_group, g.gender;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []


    labels = sorted(list(set(row.get('age_group') for row in data)))
    genders = sorted(list(set(row.get('gender') for row in data)))
    datasets = []
    colors = ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.7)']

    for i, gender in enumerate(genders):
        gender_data = []
        for label in labels:
            count = next((item.get('count', 0) for item in data if item.get('age_group') == label and item.get('gender') == gender), 0)
            gender_data.append(count)
        datasets.append({
            'label': gender,
            'data': gender_data,
            'backgroundColor': colors[i % len(colors)],
            'borderColor': colors[i % len(colors)].replace('0.7', '1'),
            'borderWidth': 1
        })

    chart_data = {
        'labels': labels,
        'datasets': datasets
    }
    return JsonResponse(chart_data)

def smp_occupation_income_profile(request, platform_id):
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS user_count,
            ROUND(AVG(u.monthly_income), 2) AS avg_income
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.primary_plat_id = %s
        GROUP BY o.occupation_name
        ORDER BY user_count DESC
        LIMIT 7;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []

    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'datasets': [
            {
                'label': 'Número de Usuarios',
                'data': [row.get('user_count', 0) for row in data],
                'backgroundColor': 'rgba(75, 192, 192, 0.7)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'yAxisID': 'y_users',
                'borderWidth': 1,
                'type': 'bar'
            },
            {
                'label': 'Ingreso Promedio ($)',
                'data': [row.get('avg_income', 0) for row in data],
                'backgroundColor': 'rgba(255, 159, 64, 0.7)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'yAxisID': 'y_income',
                'borderWidth': 1,
                'type': 'line',
                'tension': 0.1
            }
        ]
    }
    return JsonResponse(chart_data)


def smp_content_affinity(request, platform_id):
    query = """
        SELECT
            e.entertainment_name,
            COUNT(u.user_id) AS user_count
        FROM users u
        JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
        WHERE u.primary_plat_id = %s
        GROUP BY e.entertainment_name
        ORDER BY user_count DESC;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('entertainment_name', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)


def smp_user_intent(request, platform_id):
    query = """
        SELECT
            mg.goal_name,
            COUNT(u.user_id) AS user_count
        FROM users u
        JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
        WHERE u.primary_plat_id = %s
        GROUP BY mg.goal_name
        ORDER BY user_count DESC;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('goal_name', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)


def smp_engagement_spending_profile(request, platform_id):
    query = """
        SELECT
            CASE
                WHEN u.d_sm_time < 1 THEN 'Menos de 1h'
                WHEN u.d_sm_time BETWEEN 1 AND 2 THEN '1-2h'
                WHEN u.d_sm_time BETWEEN 2 AND 3 THEN '2-3h'
                WHEN u.d_sm_time BETWEEN 3 AND 4 THEN '3-4h'
                WHEN u.d_sm_time BETWEEN 4 AND 5 THEN '4-5h'
                ELSE 'Más de 5h'
            END AS time_bin,
            COUNT(u.user_id) AS user_count,
            ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spending
        FROM users u
        WHERE u.primary_plat_id = %s
        GROUP BY time_bin
        ORDER BY
            CASE time_bin
                WHEN 'Menos de 1h' THEN 1
                WHEN '1-2h' THEN 2
                WHEN '2-3h' THEN 3
                WHEN '3-4h' THEN 4
                WHEN '4-5h' THEN 5
                WHEN 'Más de 5h' THEN 6
                ELSE 7
            END;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []

    chart_data = {
        'labels': [row.get('time_bin', 'N/A') for row in data],
        'datasets': [{
            'label': 'Gasto Promedio en Entretenimiento ($)',
            'data': [row.get('avg_spending', 0) for row in data],
            'backgroundColor': 'rgba(153, 102, 255, 0.7)',
            'borderColor': 'rgba(153, 102, 255, 1)',
            'borderWidth': 1,

        }]
    }
    return JsonResponse(chart_data)

def smp_device_profile(request, platform_id):
    query_sm = """
        SELECT d.device_name, COUNT(u.user_id) as count
        FROM users u JOIN devices d ON u.device_sm_id = d.device_id
        WHERE u.primary_plat_id = %s
        GROUP BY d.device_name ORDER BY count DESC;
    """
    query_ent = """
        SELECT d.device_name, COUNT(u.user_id) as count
        FROM users u JOIN devices d ON u.devide_for_entertainment_id = d.device_id
        WHERE u.primary_plat_id = %s
        GROUP BY d.device_name ORDER BY count DESC;
    """
    data_sm = execute_query(query_sm, [platform_id])
    data_ent = execute_query(query_ent, [platform_id])
    if not isinstance(data_sm, list): data_sm = []
    if not isinstance(data_ent, list): data_ent = []

    chart_data = {
        'sm_devices': {
            'labels': [row.get('device_name', 'N/A') for row in data_sm],
            'data': [row.get('count', 0) for row in data_sm]
        },
        'ent_devices': {
            'labels': [row.get('device_name', 'N/A') for row in data_ent],
            'data': [row.get('count', 0) for row in data_ent]
        }
    }
    return JsonResponse(chart_data)


def country_income_distribution(request, country_id):
    query = """
        SELECT
            CASE
                WHEN monthly_income < 2000 THEN '< $2000'
                WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000 - $3999'
                WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000 - $5999'
                WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000 - $7999'
                ELSE '$8000+'
            END AS income_bracket,
            COUNT(user_id) AS user_count
        FROM users
        WHERE country_id = %s
        GROUP BY income_bracket
        ORDER BY
            CASE income_bracket
                WHEN '< $2000' THEN 1
                WHEN '$2000 - $3999' THEN 2
                WHEN '$4000 - $5999' THEN 3
                WHEN '$6000 - $7999' THEN 4
                WHEN '$8000+' THEN 5
                ELSE 6
            END;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('income_bracket', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_spending_distribution(request, country_id):
    query = """
        SELECT
            CASE
                WHEN monthly_spent_entertain < 50 THEN '< $50'
                WHEN monthly_spent_entertain BETWEEN 50 AND 99 THEN '$50 - $99'
                WHEN monthly_spent_entertain BETWEEN 100 AND 149 THEN '$100 - $149'
                WHEN monthly_spent_entertain BETWEEN 150 AND 199 THEN '$150 - $199'
                ELSE '$200+'
            END AS spending_bracket,
            COUNT(user_id) AS user_count
        FROM users
        WHERE country_id = %s
        GROUP BY spending_bracket
        ORDER BY
            CASE spending_bracket
                WHEN '< $50' THEN 1
                WHEN '$50 - $99' THEN 2
                WHEN '$100 - $149' THEN 3
                WHEN '$150 - $199' THEN 4
                WHEN '$200+' THEN 5
                ELSE 6
            END;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('spending_bracket', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)


def country_occupation_landscape(request, country_id):
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS user_count
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.country_id = %s
        GROUP BY o.occupation_name
        ORDER BY user_count DESC
        LIMIT 10;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)


def country_lifestyle_indicators(request, country_id):
    query = """
        SELECT
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep,
            ROUND(AVG(physical_activity_tiem), 1) AS avg_activity,
            ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
            ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
        FROM users
        WHERE country_id = %s;
    """
    data = execute_query(query, [country_id])
    result = {}
    if isinstance(data, dict):
        result = {k: (v if v is not None else 'N/A') for k, v in data.items()}
    elif isinstance(data, (list, tuple)) and len(data) >= 4:
        result = {
            'avg_sleep': data[0] if data[0] is not None else 'N/A',
            'avg_activity': data[1] if data[1] is not None else 'N/A',
            'avg_notifications': data[2] if data[2] is not None else 'N/A',
            'avg_tech_savviness': data[3] if data[3] is not None else 'N/A'
        }
    else:
          result = {'avg_sleep': 'N/A', 'avg_activity': 'N/A', 'avg_notifications': 'N/A', 'avg_tech_savviness': 'N/A'}

    return JsonResponse(result)

def country_tech_savviness_distribution(request, country_id):
    query = """
        SELECT
            tech_savviness_level,
            COUNT(user_id) AS user_count
        FROM users
        WHERE country_id = %s
        GROUP BY tech_savviness_level
        ORDER BY tech_savviness_level;
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []

    labels = [f"Nivel {row.get('tech_savviness_level', 'N/A')}" for row in data]
    chart_data = {
        'labels': labels,
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)

def country_lifestyle_indicators(request, country_id):
    query = """
        SELECT
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep,
            ROUND(AVG(physical_activity_tiem), 1) AS avg_activity,
            ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
            ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
        FROM users
        WHERE country_id = %s;
    """
    data = execute_query(query, [country_id])
    result = {}
    if isinstance(data, dict):
        result = {k: (v if v is not None else 'N/A') for k, v in data.items()}
    elif isinstance(data, (list, tuple)) and len(data) >= 4:
        result = {
            'avg_sleep': data[0] if data[0] is not None else 'N/A',
            'avg_activity': data[1] if data[1] is not None else 'N/A',
            'avg_notifications': data[2] if data[2] is not None else 'N/A',
            'avg_tech_savviness': data[3] if data[3] is not None else 'N/A'
        }
    else:
          result = {'avg_sleep': 'N/A', 'avg_activity': 'N/A', 'avg_notifications': 'N/A', 'avg_tech_savviness': 'N/A'}

    return JsonResponse(result)


def gender_platform_preference(request, gender_id):
    query_sm = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count
        FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.gender_id = %s
        GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    query_ent_plat = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count
        FROM users u JOIN social_media sm ON u.preferred_enter_plat_id = sm.socialm_id
        WHERE u.gender_id = %s
        GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    data_sm = execute_query(query_sm, [gender_id])
    data_ent_plat = execute_query(query_ent_plat, [gender_id])
    if not isinstance(data_sm, list): data_sm = []
    if not isinstance(data_ent_plat, list): data_ent_plat = []

    chart_data = {
        'primary_sm': {
            'labels': [row.get('socialm_name', 'N/A') for row in data_sm],
            'data': [row.get('count', 0) for row in data_sm]
        },
        'preferred_ent_platform': {
            'labels': [row.get('socialm_name', 'N/A') for row in data_ent_plat],
            'data': [row.get('count', 0) for row in data_ent_plat]
        }
    }
    return JsonResponse(chart_data)


def gender_income_vs_spending(request, gender_id):
    query = """
        SELECT
            CASE
                WHEN monthly_income < 2000 THEN '< $2000'
                WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000 - $3999'
                WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000 - $5999'
                WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000 - $7999'
                ELSE '$8000+'
            END AS income_bracket,
            COUNT(user_id) AS user_count,
            ROUND(AVG(monthly_spent_entertain), 2) AS avg_spending
        FROM users
        WHERE gender_id = %s
        GROUP BY income_bracket
        ORDER BY
            CASE income_bracket
                WHEN '< $2000' THEN 1 WHEN '$2000 - $3999' THEN 2 WHEN '$4000 - $5999' THEN 3
                WHEN '$6000 - $7999' THEN 4 WHEN '$8000+' THEN 5 ELSE 6
            END;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []

    chart_data = {
        'labels': [row.get('income_bracket', 'N/A') for row in data],
        'datasets': [
            {
                'label': 'Gasto Promedio en Entretenimiento ($)',
                'data': [row.get('avg_spending', 0) for row in data],
                'backgroundColor': 'rgba(255, 159, 64, 0.7)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'yAxisID': 'y_spending',
                'borderWidth': 1,
                'type': 'bar'
            },
            {
                'label': 'Número de Usuarios',
                'data': [row.get('user_count', 0) for row in data],
                'backgroundColor': 'rgba(201, 203, 207, 0.5)',
                'borderColor': 'rgba(201, 203, 207, 1)',
                'yAxisID': 'y_users',
                'borderWidth': 1,
                'type': 'line',
                'tension': 0.1
            }
        ]
    }
    return JsonResponse(chart_data)


def gender_sm_goal_distribution(request, gender_id):
    query = """
        SELECT
            mg.goal_name,
            COUNT(u.user_id) AS user_count
        FROM users u
        JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
        WHERE u.gender_id = %s
        GROUP BY mg.goal_name
        ORDER BY user_count DESC;
    """
    data = execute_query(query, [gender_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('goal_name', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)


def gender_engagement_indicators(request, gender_id):
    query = """
        SELECT
            ROUND(AVG(ad_interaction_count), 1) AS avg_ad_interactions,
            ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
            ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
        FROM users
        WHERE gender_id = %s;
    """
    data = execute_query(query, [gender_id])
    result = {}
    if isinstance(data, dict):
        result = {k: (v if v is not None else 'N/A') for k, v in data.items()}
    elif isinstance(data, (list, tuple)) and len(data) >= 3:
        result = {
            'avg_ad_interactions': data[0] if data[0] is not None else 'N/A',
            'avg_notifications': data[1] if data[1] is not None else 'N/A',
            'avg_tech_savviness': data[2] if data[2] is not None else 'N/A',
        }
    else:
          result = {'avg_ad_interactions': 'N/A', 'avg_notifications': 'N/A', 'avg_tech_savviness': 'N/A'}
    return JsonResponse(result)


def ent_core_demographics(request, entertainment_id):
    query_age = """
        SELECT CASE
            WHEN u.age BETWEEN 0 AND 17 THEN '0-17' WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
            WHEN u.age BETWEEN 26 AND 35 THEN '26-35' WHEN u.age BETWEEN 36 AND 50 THEN '36-50' ELSE '51+'
            END AS age_group, COUNT(u.user_id) AS count
        FROM users u WHERE u.preferred_content_id = %s GROUP BY age_group ORDER BY age_group;
    """
    query_gender = """
        SELECT g.gender, COUNT(u.user_id) AS count
        FROM users u JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.preferred_content_id = %s GROUP BY g.gender ORDER BY count DESC;
    """
    data_age = execute_query(query_age, [entertainment_id])
    data_gender = execute_query(query_gender, [entertainment_id])
    if not isinstance(data_age, list): data_age = []
    if not isinstance(data_gender, list): data_gender = []

    age_order = {'0-17': 1, '18-25': 2, '26-35': 3, '36-50': 4, '51+': 5}
    data_age.sort(key=lambda x: age_order.get(x.get('age_group', ''), 99))


    chart_data = {
        'age_distribution': {'labels': [r.get('age_group') for r in data_age], 'data': [r.get('count') for r in data_age]},
        'gender_distribution': {'labels': [r.get('gender') for r in data_gender], 'data': [r.get('count') for r in data_gender]}
    }
    return JsonResponse(chart_data)

def ent_socioeconomic_profile(request, entertainment_id):
    query_countries = """
        SELECT c.country_name, COUNT(u.user_id) AS count FROM users u
        JOIN countries c ON u.country_id = c.country_id
        WHERE u.preferred_content_id = %s GROUP BY c.country_name ORDER BY count DESC LIMIT 5;
    """
    query_occ = """
        SELECT o.occupation_name, COUNT(u.user_id) AS count FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.preferred_content_id = %s GROUP BY o.occupation_name ORDER BY count DESC LIMIT 7;
    """
    query_inc = """
        SELECT CASE
            WHEN monthly_income < 2000 THEN '< $2000' WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000-$3999'
            WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000-$5999' WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000-$7999'
            ELSE '$8000+'
            END AS income_bracket, COUNT(user_id) AS count
        FROM users WHERE preferred_content_id = %s GROUP BY income_bracket ORDER BY MIN(monthly_income);
    """
    data_countries = execute_query(query_countries, [entertainment_id])
    data_occ = execute_query(query_occ, [entertainment_id])
    data_inc = execute_query(query_inc, [entertainment_id])
    if not isinstance(data_countries, list): data_countries = []
    if not isinstance(data_occ, list): data_occ = []
    if not isinstance(data_inc, list): data_inc = []

    chart_data = {
        'top_countries': {'labels': [r.get('country_name') for r in data_countries], 'data': [r.get('count') for r in data_countries]},
        'top_occupations': {'labels': [r.get('occupation_name') for r in data_occ], 'data': [r.get('count') for r in data_occ]},
        'income_distribution': {'labels': [r.get('income_bracket') for r in data_inc], 'data': [r.get('count') for r in data_inc]}
    }
    return JsonResponse(chart_data)


def ent_platform_and_device(request, entertainment_id):
    query_sm_plat = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
        JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    query_ent_plat = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
        JOIN social_media sm ON u.preferred_enter_plat_id = sm.socialm_id
        WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    query_dev_ent = """
        SELECT d.device_name, COUNT(u.user_id) as count FROM users u
        JOIN devices d ON u.devide_for_entertainment_id = d.device_id
        WHERE u.preferred_content_id = %s GROUP BY d.device_name ORDER BY count DESC;
    """
    data_sm_plat = execute_query(query_sm_plat, [entertainment_id])
    data_ent_plat = execute_query(query_ent_plat, [entertainment_id])
    data_dev_ent = execute_query(query_dev_ent, [entertainment_id])
    if not isinstance(data_sm_plat, list): data_sm_plat = []
    if not isinstance(data_ent_plat, list): data_ent_plat = []
    if not isinstance(data_dev_ent, list): data_dev_ent = []

    chart_data = {
        'primary_sm_platform': {'labels': [r.get('socialm_name') for r in data_sm_plat], 'data': [r.get('count') for r in data_sm_plat]},
        'preferred_ent_platform': {'labels': [r.get('socialm_name') for r in data_ent_plat], 'data': [r.get('count') for r in data_ent_plat]},
        'device_entertainment': {'labels': [r.get('device_name') for r in data_dev_ent], 'data': [r.get('count') for r in data_dev_ent]}
    }
    return JsonResponse(chart_data)

def ent_engagement_profile(request, entertainment_id):
    query_time = "SELECT ROUND(AVG(d_entertain_time), 1) AS avg_ent, ROUND(AVG(d_sm_time), 1) AS avg_sm FROM users WHERE preferred_content_id = %s;"
    query_goal = """
        SELECT mg.goal_name, COUNT(u.user_id) AS count FROM users u JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
        WHERE u.preferred_content_id = %s GROUP BY mg.goal_name ORDER BY count DESC; """
    query_life = """
        SELECT ROUND(AVG(subscription_plats),1) AS avg_subs, ROUND(AVG(avg_sleep_time),1) AS avg_sleep,
               ROUND(AVG(physical_activity_tiem),1) AS avg_activity, ROUND(AVG(tech_savviness_level),1) AS avg_tech
        FROM users WHERE preferred_content_id = %s; """

    data_time = execute_query(query_time, [entertainment_id])
    data_goal = execute_query(query_goal, [entertainment_id])
    data_life = execute_query(query_life, [entertainment_id])
    if not isinstance(data_goal, list): data_goal = []

    time_labels = ['Tiempo Entretenimiento', 'Tiempo Redes Sociales']
    time_data = [0, 0]
    if isinstance(data_time, dict): time_data = [data_time.get('avg_ent', 0), data_time.get('avg_sm', 0)]
    elif isinstance(data_time, tuple): time_data = [data_time[0] if data_time[0] else 0, data_time[1] if data_time[1] else 0]

    life_indicators = {'avg_subs':'N/A', 'avg_sleep': 'N/A', 'avg_activity': 'N/A', 'avg_tech': 'N/A'}
    if isinstance(data_life, dict): life_indicators = {k: (v if v is not None else 'N/A') for k, v in data_life.items()}
    elif isinstance(data_life, tuple): life_indicators = {'avg_subs': data_life[0] if data_life[0] else 'N/A', 'avg_sleep': data_life[1] if data_life[1] else 'N/A', 'avg_activity': data_life[2] if data_life[2] else 'N/A', 'avg_tech': data_life[3] if data_life[3] else 'N/A'}

    chart_data = {
        'time_comparison': {'labels': time_labels, 'data': time_data},
        'sm_goal': {'labels': [r.get('goal_name') for r in data_goal], 'data': [r.get('count') for r in data_goal]},
        'lifestyle_and_subs': life_indicators
    }
    return JsonResponse(chart_data)

def auxMenu():
    redesSociales = SocialMedia.objects.all().order_by('socialm_name').values()
    paises = Countries.objects.all().order_by('country_name').values()
    generos = Gender.objects.all().order_by('gender').values()
    tipoEntretenimiento = Entretaiment.objects.all().order_by('entertainment_name').values()
    return redesSociales, paises, generos, tipoEntretenimiento

def get_total_users_count():
    query = "SELECT COUNT(*) AS count FROM users;"
    result = execute_query(query)
    return result[0]['count'] if result else 0

def get_avg_age_value():
    query = "SELECT ROUND(AVG(age), 1) AS avg_age FROM users;"
    result = execute_query(query)
    return result[0]['avg_age'] if result else 'N/A'

def get_avg_income_value():
    query = "SELECT ROUND(AVG(monthly_income), 2) AS avg_income FROM users;"
    result = execute_query(query)
    return result[0]['avg_income'] if result else 'N/A'

def get_top_platforms_distribution(request):
    query = """
        SELECT sm.socialm_name, COUNT(u.user_id) AS user_count
        FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        GROUP BY sm.socialm_name ORDER BY user_count DESC;
    """
    data = execute_query(query)
    chart_data = {
        'labels': [r.get('socialm_name', 'N/A') for r in data],
        'data': [r.get('user_count', 0) for r in data]
    }
    return JsonResponse(chart_data)

def get_top_entertainment_distribution(request):
    query = """
        SELECT e.entertainment_name, COUNT(u.user_id) AS user_count
        FROM users u JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
        GROUP BY e.entertainment_name ORDER BY user_count DESC;
    """
    data = execute_query(query)
    chart_data = {
        'labels': [r.get('entertainment_name', 'N/A') for r in data],
        'data': [r.get('user_count', 0) for r in data]
    }
    return JsonResponse(chart_data)

def get_users_by_country_distribution(request):
    query = """
        SELECT c.country_name, COUNT(u.user_id) AS user_count
        FROM users u JOIN countries c ON u.country_id = c.country_id
        GROUP BY c.country_name ORDER BY user_count DESC LIMIT 10;
    """
    data = execute_query(query)
    chart_data = {
        'labels': [r.get('country_name', 'N/A') for r in data],
        'data': [r.get('user_count', 0) for r in data]
    }
    return JsonResponse(chart_data)

def get_platform_highest_avg_income(request):
    query = """
        SELECT sm.socialm_name, ROUND(AVG(u.monthly_income), 2) AS avg_income
        FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        GROUP BY sm.socialm_name
        HAVING COUNT(u.user_id) > 2
        ORDER BY avg_income DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result)

def get_platform_for_highest_tech_savvy(request):
    query = """
        WITH RankedTech AS (
            SELECT primary_plat_id, AVG(tech_savviness_level) AS avg_tech
            FROM users GROUP BY primary_plat_id HAVING COUNT(user_id) > 2
        )
        SELECT sm.socialm_name, rt.avg_tech
        FROM RankedTech rt JOIN social_media sm ON rt.primary_plat_id = sm.socialm_id
        ORDER BY rt.avg_tech DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result)

def get_avg_subscriptions_per_income_bracket(request):
    query = """
        SELECT
            CASE
                WHEN monthly_income < 2000 THEN '< $2000' WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2k-$4k'
                WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4k-$6k' WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6k-$8k'
                ELSE '$8k+' END AS income_bracket,
            ROUND(AVG(subscription_plats), 1) AS avg_subs
        FROM users GROUP BY income_bracket ORDER BY MIN(monthly_income);
    """
    data = execute_query(query)
    income_order = {'< $2000': 1, '$2k-$4k': 2, '$4k-$6k': 3, '$6k-$8k': 4, '$8k+': 5}
    data_filtered = [item for item in data if item.get('income_bracket') is not None]
    data_filtered.sort(key=lambda x: income_order.get(x.get('income_bracket', ''), 99))

    chart_data = {
        'labels': [r.get('income_bracket', 'N/A') for r in data_filtered],
        'data': [r.get('avg_subs', 0) for r in data_filtered]
    }
    return JsonResponse(chart_data)

def get_sleep_quality_by_notification_level(request):
    avg_notif_query = "SELECT AVG(d_num_notifications) FROM users;"
    avg_notif_result = execute_query(avg_notif_query)
    threshold = avg_notif_result[0]['result'] if avg_notif_result and avg_notif_result[0].get('result') is not None else 50

    query = f"""
        SELECT
            CASE WHEN d_num_notifications > {threshold} THEN 'Notificaciones Altas (> {int(threshold)})' ELSE 'Notificaciones Bajas (<= {int(threshold)})' END AS notif_level,
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep
        FROM users GROUP BY notif_level ORDER BY notif_level;
    """
    data = execute_query(query)
    result = {item.get('notif_level'): item.get('avg_sleep') for item in data}
    return JsonResponse(result)

def get_sm_time_by_gaming_level(request):

    threshold = 1.0
    query = f"""
        SELECT
            CASE WHEN d_gaming_time > {threshold} THEN 'Gamers (> {threshold}h)' ELSE 'No/Poco Gamers (<= {threshold}h)' END AS gaming_level,
            ROUND(AVG(d_sm_time), 1) AS avg_sm_time
        FROM users GROUP BY gaming_level ORDER BY gaming_level;
    """
    data = execute_query(query)
    result = {item.get('gaming_level'): item.get('avg_sm_time') for item in data}
    return JsonResponse(result)

def get_age_group_highest_ad_interaction(request):
    query = """
        SELECT
             CASE WHEN age <= 17 THEN '0-17' WHEN age <= 25 THEN '18-25' WHEN age <= 35 THEN '26-35'
                   WHEN age <= 50 THEN '36-50' ELSE '51+' END AS age_group,
             ROUND(AVG(ad_interaction_count), 1) AS avg_interactions
        FROM users GROUP BY age_group ORDER BY avg_interactions DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result)

def get_occupation_distinct_entertainment(request):

    query = """
          WITH OccPref AS (
              SELECT occupation_id, preferred_content_id, COUNT(user_id) AS group_count
              FROM users GROUP BY occupation_id, preferred_content_id
          ), TotalOcc AS (
              SELECT occupation_id, COUNT(user_id) AS total_in_occ FROM users GROUP BY occupation_id
          ), OverallPref AS (
              SELECT preferred_content_id, COUNT(user_id) * 1.0 / (SELECT COUNT(*) FROM users) AS overall_ratio
              FROM users GROUP BY preferred_content_id
          )
          SELECT o.occupation_name, e.entertainment_name,
                 (op.group_count * 1.0 / toc.total_in_occ) / ovp.overall_ratio AS distinct_ratio
          FROM OccPref op
          JOIN TotalOcc toc ON op.occupation_id = toc.occupation_id
          JOIN OverallPref ovp ON op.preferred_content_id = ovp.preferred_content_id
          JOIN occupations o ON op.occupation_id = o.occupation_id
          JOIN entretaiment e ON op.preferred_content_id = e.entertainment_id
          WHERE ovp.overall_ratio > 0 AND toc.total_in_occ > 2
          ORDER BY distinct_ratio DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result)

def get_country_highest_screen_time(request):
    query = """
        SELECT c.country_name, ROUND(AVG(u.screen_time), 1) AS avg_screen_time
        FROM users u JOIN countries c ON u.country_id = c.country_id
        GROUP BY c.country_name HAVING COUNT(u.user_id) > 2
        ORDER BY avg_screen_time DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result)

def main(request):
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    context = {
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento,

        'total_users_metric' : get_total_users_count(),
        'avg_age_metric': get_avg_age_value(),
        'avg_income_metric': get_avg_income_value(),
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))



def redsocial(request, id):

    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    platform = SocialMedia.objects.get(pk=id)
    context = {'platform_id': id, 'platform_name': platform.socialm_name, 'titulo': platform.socialm_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('smp.html')
    return HttpResponse(template.render(context, request))

def countriesDetail(request, id):

    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    country = Countries.objects.get(pk=id)
    context = {'country_id': id, 'country_name': country.country_name, 'titulo': country.country_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('paises.html')
    return HttpResponse(template.render(context, request))

def genderDetail(request, id):

    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    gender = Gender.objects.get(pk=id)
    context = {'gender_id': id, 'gender_name': gender.gender, 'titulo': gender.gender.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('generos.html')
    return HttpResponse(template.render(context, request))

def entertainmentDetail(request, id):

    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    entertainment = Entretaiment.objects.get(pk=id)
    context = {'entertainment_id': id, 'entertainment_name': entertainment.entertainment_name, 'titulo': entertainment.entertainment_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('entretenimiento.html')
    return HttpResponse(template.render(context, request))