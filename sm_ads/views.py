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
    total_users_entr = Users.objects.raw('''SELECT COUNT(*) AS total_users FROM users;''')
    

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
        'suegno_vs_tiempopant' : suegno_vs_tiempopant,
        'total_users_entr' : get_total_users(),
        'avg_age': get_avg_age(),
        'top_social_media': get_top_social_media(),
        'avg_income': get_avg_income(),
        'top_country': get_top_country(),
        'top_device': get_top_device(),
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
    
def get_total_users():
    with connection.cursor() as cursor:
        #ya no definimo el query como string sino que ya lo estamos metiendo directo en el cursor.execute
        cursor.execute("SELECT COUNT(*) FROM users;")
        return cursor.fetchone()[0]
    

# Edad promedio
def get_avg_age():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ROUND(AVG(age), 1) FROM users;")
        return cursor.fetchone()[0]

# Plataforma de redes sociales más usada (por ID)
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

# Ingreso mensual promedio
def get_avg_income():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ROUND(AVG(monthly_income), 2) FROM users;")
        return cursor.fetchone()[0]

# País con más usuarios (por ID)
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

# Dispositivo más usado (por ID)
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
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados como lista de diccionarios."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            return dictfetchall(cursor)
        # Para consultas que no devuelven filas (como COUNT(*)) pero sí un valor
        elif cursor.rowcount > 0 or cursor.fetchone() is not None:
             # Re-ejecutar si fetchone consumió el resultado de una consulta simple
             cursor.execute(query, params)
             result = cursor.fetchone()
             # Si la consulta devuelve una sola columna (ej. COUNT)
             if result and len(result) == 1:
                 return result[0]
             return result # Devuelve la tupla si hay más columnas
        else:
            return [] # O None, según prefieras manejar sin resultados

# --- API Views for Social Media Platform Details ---

def smp_age_distribution(request, platform_id):
    """Distribución de edad para una plataforma específica."""
    query = """
        -- Distribución de edad para la plataforma seleccionada
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
    # print(f"Executing smp_age_distribution with platform_id: {platform_id}") # Debug
    data = execute_query(query, [platform_id])
    # print(f"Data returned: {data}") # Debug

    # Asegurarse de que data sea una lista de diccionarios
    if not isinstance(data, list):
        data = [] # O manejar el error como sea apropiado

    chart_data = {
        'labels': [row.get('age_group', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip() # Incluir la consulta para mostrarla si se desea
    }
    return JsonResponse(chart_data)

def smp_gender_distribution(request, platform_id):
    """Distribución de género para una plataforma específica."""
    query = """
        -- Distribución de género para la plataforma seleccionada
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

    # Asegurarse de que data sea una lista de diccionarios
    if not isinstance(data, list):
        data = []

    chart_data = {
        'labels': [row.get('gender', 'N/A') for row in data],
        'data': [row.get('total_users', 0) for row in data],
        'query': query.strip()
    }
    return JsonResponse(chart_data)

def smp_top_countries(request, platform_id):
    """Top 10 países para una plataforma específica."""
    query = """
        -- Top 10 países por usuarios para la plataforma seleccionada
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
    """Top 10 ocupaciones para una plataforma específica."""
    query = """
        -- Top 10 ocupaciones por usuarios para la plataforma seleccionada
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

# --- Actualiza la vista socialMediaPlatform ---
def socialMediaPlatform(request, id): # 'id' aquí es platform_id
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('smp.html')
    titulo = ''
    platform_name = 'Plataforma Desconocida' # Valor por defecto
    try:
        platform = SocialMedia.objects.get(pk=id)
        platform_name = platform.socialm_name
        titulo = platform_name.upper()
    except SocialMedia.DoesNotExist:
        # Manejar el caso donde el ID no existe si es necesario
        # Podrías redirigir a 404 o mostrar un mensaje
        pass # Por ahora, usa el título por defecto

    context = {
     'redesSociales': redesSociales,
     'paises': paises,
     'generos': generos,
     'tipoEntretenimiento': tipoEntretenimiento,
     'titulo': titulo,
     'platform_name': platform_name, # Nombre para mostrar
     'platform_id': id, # Pasar el ID a la plantilla para las llamadas API
    }
    return HttpResponse(template.render(context, request))

# views.py (añadir estas funciones, asegúrate de tener 'dictfetchall' y 'execute_query' definidas como en la respuesta anterior)

# --- API Views for Country Details ---

def country_age_distribution(request, country_id):
    """Distribución de edad para un país específico."""
    query = """
        -- Distribución de edad para el país seleccionado
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
    """Distribución de género para un país específico."""
    query = """
        -- Distribución de género para el país seleccionado
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
    """Top plataformas de redes sociales para un país específico."""
    query = """
        -- Top 5 Redes Sociales para el país seleccionado
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
    """Top tipos de entretenimiento para un país específico."""
    query = """
        -- Top 5 Tipos de Entretenimiento para el país seleccionado
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
    """Tiempo promedio en SM vs Entretenimiento para un país."""
    query = """
        -- Tiempo Promedio Diario (Horas): Redes Sociales vs Entretenimiento
        SELECT
            ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
            ROUND(AVG(u.d_entertain_time), 2) AS avg_ent_time
        FROM users u
        WHERE u.country_id = %s;
    """
    # execute_query puede devolver un diccionario aquí si se adapta o la primera fila directamente
    data = execute_query(query, [country_id])

    # Asegurarse de que data sea un diccionario o una tupla/lista con los valores
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
    """Ingreso vs Gasto promedio en entretenimiento para un país."""
    query = """
        -- Ingreso Mensual Promedio vs Gasto Promedio en Entretenimiento
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

# --- Actualiza la vista countriesDetail ---
def countriesDetail(request, id): # 'id' aquí es country_id
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('paises.html')
    titulo = ''
    country_name = 'País Desconocido' # Valor por defecto
    try:
        # Asumiendo que tienes un modelo Countries importado
        country = Countries.objects.get(pk=id)
        country_name = country.country_name
        titulo = country_name.upper()
    except Countries.DoesNotExist:
        pass # Manejar si el país no existe

    context = {
      'redesSociales': redesSociales,
      'paises': paises,
      'generos': generos,
      'tipoEntretenimiento': tipoEntretenimiento,
      'titulo': titulo,
      'country_name': country_name,
      'country_id': id, # Pasar el ID a la plantilla
    }
    return HttpResponse(template.render(context, request))

# views.py (añadir estas funciones, asegúrate de tener 'dictfetchall' y 'execute_query')

# --- API Views for Gender Details ---

def gender_age_distribution(request, gender_id):
    """Distribución de edad para un género específico."""
    query = """
        -- Distribución de edad para el género seleccionado
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
    """Top 5 plataformas de redes sociales para un género específico."""
    query = """
        -- Top 5 Redes Sociales para el género seleccionado
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
    """Top 5 tipos de entretenimiento para un género específico."""
    query = """
        -- Top 5 Tipos de Entretenimiento para el género seleccionado
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
    """Top 5 ocupaciones para un género específico."""
    query = """
        -- Top 5 Ocupaciones para el género seleccionado
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
    """Tiempo promedio en SM vs Entretenimiento para un género."""
    query = """
        -- Tiempo Promedio Diario (Horas) para el género seleccionado
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
    """Ingreso vs Gasto promedio en entretenimiento para un género."""
    query = """
        -- Ingreso Mensual Promedio vs Gasto Promedio en Entretenimiento para el género seleccionado
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


# --- Actualiza la vista genderDetail ---
def genderDetail(request, id): # 'id' aquí es gender_id
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('generos.html')
    titulo = ''
    gender_name = 'Género Desconocido' # Valor por defecto
    try:
        # Asumiendo que tienes un modelo Gender importado
        gender_obj = Gender.objects.get(pk=id)
        gender_name = gender_obj.gender # El campo se llama 'gender' en tu modelo
        titulo = gender_name.upper()
    except Gender.DoesNotExist:
        pass # Manejar si el género no existe

    context = {
       'redesSociales': redesSociales,
       'paises': paises,
       'generos': generos, # La lista completa para la sidebar
       'tipoEntretenimiento': tipoEntretenimiento,
       'titulo': titulo, # Para el header (ej. MALE)
       'gender_name': gender_name, # Nombre descriptivo (ej. Male)
       'gender_id': id, # Pasar el ID a la plantilla
    }
    return HttpResponse(template.render(context, request))

# views.py (añadir estas funciones, asegúrate de tener 'dictfetchall' y 'execute_query')

# --- API Views for Entertainment Type Details ---

def ent_age_distribution(request, entertainment_id):
    """Distribución de edad para usuarios que prefieren un tipo de entretenimiento."""
    query = """
        -- Distribución de edad para el tipo de entretenimiento seleccionado
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
    """Distribución de género para usuarios que prefieren un tipo de entretenimiento."""
    query = """
        -- Distribución de género para el tipo de entretenimiento seleccionado
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
    """Top 5 países donde se prefiere este tipo de entretenimiento."""
    # Usamos el query de service_queries.sql como referencia
    query = """
        -- Top 5 Países donde se prefiere este entretenimiento
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
    """Top 5 plataformas de redes sociales usadas por quienes prefieren este entretenimiento."""
    query = """
        -- Top 5 Redes Sociales usadas por quienes prefieren este entretenimiento
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
    """Top 5 ocupaciones de quienes prefieren este entretenimiento."""
    query = """
        -- Top 5 Ocupaciones de quienes prefieren este entretenimiento
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
    """Dispositivos usados para entretenimiento por quienes prefieren este tipo."""
    # Usamos el campo 'devide_for_entertainment_id'
    query = """
        -- Dispositivos usados para entretenimiento por quienes prefieren este tipo
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

# --- Actualiza la vista entertainmentDetail ---
def entertainmentDetail(request, id): # 'id' aquí es entertainment_id
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    template = loader.get_template('entretenimiento.html')
    titulo = ''
    entertainment_name = 'Tipo Desconocido' # Valor por defecto
    try:
        # Asumiendo que tienes un modelo Entretaiment importado
        entertainment_obj = Entretaiment.objects.get(pk=id)
        entertainment_name = entertainment_obj.entertainment_name
        titulo = entertainment_name.upper()
    except Entretaiment.DoesNotExist:
        pass # Manejar si el tipo no existe

    context = {
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento, # Lista para sidebar
        'titulo': titulo, # Para header (ej. NEWS)
        'entertainment_name': entertainment_name, # Nombre descriptivo (ej. News)
        'entertainment_id': id, # Pasar el ID a la plantilla
    }
    return HttpResponse(template.render(context, request))

