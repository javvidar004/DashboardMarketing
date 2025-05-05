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


# views.py (AÑADIR estas nuevas vistas API, asegúrate de tener 'dictfetchall' y 'execute_query')
#           (Puedes comentar o eliminar las API 'smp_' anteriores si no las vas a usar)

from django.db.models import Avg, Count # Usar ORM para simplificar algunas queries si se quiere

# --- API Views for Social Media Platform Marketing Insights ---

def smp_age_gender_distribution(request, platform_id):
    """Distribución de usuarios por Edad y Género para esta plataforma."""
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

    # Procesar para un gráfico de barras agrupadas o heatmap
    # Para barras agrupadas: Necesitamos etiquetas (age_group) y datasets (uno por género)
    labels = sorted(list(set(row.get('age_group') for row in data)))
    genders = sorted(list(set(row.get('gender') for row in data)))
    datasets = []
    colors = ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.7)'] # Colores para géneros

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
    """Top ocupaciones en esta plataforma y su ingreso promedio."""
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
        LIMIT 7; -- Top 7 ocupaciones
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
                'yAxisID': 'y_users', # Eje Y izquierdo para usuarios
                'borderWidth': 1,
                'type': 'bar' # Especificar tipo para eje mixto
            },
            {
                'label': 'Ingreso Promedio ($)',
                'data': [row.get('avg_income', 0) for row in data],
                'backgroundColor': 'rgba(255, 159, 64, 0.7)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'yAxisID': 'y_income', # Eje Y derecho para ingresos
                'borderWidth': 1,
                'type': 'line', # Tipo línea para superponer
                'tension': 0.1 # Suavizar la línea
            }
        ]
    }
    return JsonResponse(chart_data)


def smp_content_affinity(request, platform_id):
    """Preferencia de contenido de entretenimiento de los usuarios de esta plataforma."""
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
    # Podríamos calcular la afinidad vs promedio general aquí si fuera necesario
    return JsonResponse(chart_data)


def smp_user_intent(request, platform_id):
    """Objetivo principal de uso de redes sociales para usuarios de esta plataforma."""
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


# views.py (REEMPLAZAR esta función en sm_ads/views.py)

def smp_engagement_spending_profile(request, platform_id):
    """
    Calcula el gasto PROMEDIO en entretenimiento para diferentes RANGOS
    de tiempo de uso diario de redes sociales, para usuarios de esta plataforma.
    """
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
            COUNT(u.user_id) AS user_count, -- Contar usuarios en el rango
            ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spending
        FROM users u
        WHERE u.primary_plat_id = %s
        GROUP BY time_bin
        -- Asegurar un orden lógico para los rangos de tiempo
        ORDER BY
            CASE time_bin
                WHEN 'Menos de 1h' THEN 1
                WHEN '1-2h' THEN 2
                WHEN '2-3h' THEN 3
                WHEN '3-4h' THEN 4
                WHEN '4-5h' THEN 5
                WHEN 'Más de 5h' THEN 6
                ELSE 7 -- Otros casos si los hubiera
            END;
    """
    data = execute_query(query, [platform_id])
    if not isinstance(data, list): data = []

    # Preparar datos para un gráfico de barras o líneas
    chart_data = {
        'labels': [row.get('time_bin', 'N/A') for row in data],
        'datasets': [{
            'label': 'Gasto Promedio en Entretenimiento ($)',
            'data': [row.get('avg_spending', 0) for row in data],
            'backgroundColor': 'rgba(153, 102, 255, 0.7)', # Color violeta
            'borderColor': 'rgba(153, 102, 255, 1)',
            'borderWidth': 1,
            # Podríamos añadir 'user_count' a tooltips si quisiéramos
            # 'tooltips_extra': [f"Usuarios en rango: {row.get('user_count', 0)}" for row in data]
        }]
        # Ya no es tipo scatter, es tipo bar o line
    }
    return JsonResponse(chart_data)

def smp_device_profile(request, platform_id):
    """Dispositivos usados para SM y Entretenimiento por usuarios de esta plataforma."""
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


# views.py (AÑADIR estas nuevas vistas API, puedes comentar/eliminar las 'country_' anteriores)

# --- API Views for Country Marketing Insights ---

def country_income_distribution(request, country_id):
    """Distribución de ingresos mensuales para este país."""
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
        ORDER BY -- Ordenar por rango de ingreso
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
    """Distribución de gasto mensual en entretenimiento para este país."""
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
        ORDER BY -- Ordenar por rango de gasto
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
    """Paisaje de ocupaciones en este país."""
    query = """
        SELECT
            o.occupation_name,
            COUNT(u.user_id) AS user_count
        FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.country_id = %s
        GROUP BY o.occupation_name
        ORDER BY user_count DESC
        LIMIT 10; -- Top 10 ocupaciones
    """
    data = execute_query(query, [country_id])
    if not isinstance(data, list): data = []
    chart_data = {
        'labels': [row.get('occupation_name', 'N/A') for row in data],
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)

# def country_time_allocation(request, country_id):
#     """Distribución promedio del tiempo diario en este país."""
#     # Ojo: physical_activity_tiem tiene typo en BBDD/Modelo
#     query = """
#         SELECT
#             ROUND(AVG(d_sm_time), 1) AS sm_time,
#             ROUND(AVG(d_entertain_time), 1) AS entertain_time,
#             ROUND(AVG(work_study_time), 1) AS work_study_time,
#             ROUND(AVG(d_gaming_time), 1) AS gaming_time,
#             ROUND(AVG(reading_time), 1) AS reading_time,
#             ROUND(AVG(physical_activity_tiem), 1) AS activity_time -- Corregir typo si se arregla en BBDD
#         FROM users
#         WHERE country_id = %s;
#     """
#     data = execute_query(query, [country_id]) # Devuelve una sola fila/dict
#     result = {}
#     if isinstance(data, dict):
#         result = {
#             'labels': ['Redes Sociales', 'Entretenimiento', 'Trabajo/Estudio', 'Videojuegos', 'Lectura', 'Act. Física'],
#             'data': [
#                 data.get('sm_time', 0), data.get('entertain_time', 0), data.get('work_study_time', 0),
#                 data.get('gaming_time', 0), data.get('reading_time', 0), data.get('activity_time', 0)
#             ]
#         }
#     elif isinstance(data, (list, tuple)) and len(data) >= 6: # Si devuelve tupla
#          result = {
#             'labels': ['Redes Sociales', 'Entretenimiento', 'Trabajo/Estudio', 'Videojuegos', 'Lectura', 'Act. Física'],
#             'data': [d if d is not None else 0 for d in data[:6]]
#          }
#     else:
#          result = {'labels': [], 'data': []}

#     return JsonResponse(result)

def country_lifestyle_indicators(request, country_id):
    """Indicadores promedio de estilo de vida (sueño, actividad, notificaciones, tech)."""
    query = """
        SELECT
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep,
            ROUND(AVG(physical_activity_tiem), 1) AS avg_activity, -- Cuidado con typo
            ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
            ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
        FROM users
        WHERE country_id = %s;
    """
    data = execute_query(query, [country_id])
    result = {}
    # Devolver directamente el diccionario/tupla resultante
    if isinstance(data, dict):
        result = data
    elif isinstance(data, (list, tuple)) and len(data) >= 4:
        result = { # Reconstruir dict si es tupla
            'avg_sleep': data[0], 'avg_activity': data[1],
            'avg_notifications': data[2], 'avg_tech_savviness': data[3]
        }
    return JsonResponse(result) # Devolver los valores para mostrar en tarjetas

# --- Vistas API Reutilizadas (Asegúrate que existan y funcionen) ---
# country_top_platforms(request, country_id) # Ya la tenías, devuelve labels y data
# country_top_entertainment(request, country_id) # Ya la tenías, devuelve labels y data
# country_age_gender_distribution(request, country_id) # Es la misma lógica que smp_age_gender_distribution

# --- Puedes crear una nueva vista para Edad/Género si quieres mantenerlas separadas ---
# def country_age_gender_mix(request, country_id):
#     """Distribución por edad y género para este país."""
#     query = """
#         SELECT
#             CASE
#                 WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
#                 WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
#                 WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
#                 WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
#                 ELSE '51+'
#             END AS age_group,
#             g.gender,
#             COUNT(u.user_id) AS count
#         FROM users u
#         JOIN gender g ON u.gender_id = g.gender_id
#         WHERE u.country_id = %s
#         GROUP BY age_group, g.gender
#         ORDER BY age_group, g.gender;
#     """
#     data = execute_query(query, [country_id])
#     if not isinstance(data, list): data = []
#     # Procesar igual que en smp_age_gender_distribution
#     labels = sorted(list(set(row.get('age_group') for row in data)))
#     genders = sorted(list(set(row.get('gender') for row in data)))
#     datasets = []
#     colors = ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.7)']
#     for i, gender in enumerate(genders):
#         gender_data = []
#         for label in labels:
#             count = next((item.get('count', 0) for item in data if item.get('age_group') == label and item.get('gender') == gender), 0)
#             gender_data.append(count)
#         datasets.append({'label': gender, 'data': gender_data, 'backgroundColor': colors[i % len(colors)], 'borderColor': colors[i % len(colors)].replace('0.7', '1'), 'borderWidth': 1})
#     chart_data = {'labels': labels, 'datasets': datasets}
#     return JsonResponse(chart_data)

# views.py (AÑADIR esta función y ELIMINAR/COMENTAR country_age_gender_mix)

def country_tech_savviness_distribution(request, country_id):
    """Distribución del nivel de habilidad tecnológica (1-5) en este país."""
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

    # Crear etiquetas explícitas para los niveles
    labels = [f"Nivel {row.get('tech_savviness_level', 'N/A')}" for row in data]
    chart_data = {
        'labels': labels,
        'data': [row.get('user_count', 0) for row in data],
    }
    return JsonResponse(chart_data)

# Asegúrate que country_lifestyle_indicators está correcta:
def country_lifestyle_indicators(request, country_id):
    """Indicadores promedio de estilo de vida (sueño, actividad, notificaciones, tech)."""
    query = """
        SELECT
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep,
            ROUND(AVG(physical_activity_tiem), 1) AS avg_activity, -- Cuidado con typo
            ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
            ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
        FROM users
        WHERE country_id = %s;
    """
    data = execute_query(query, [country_id])
    result = {}
    # Devolver directamente el diccionario/tupla resultante
    if isinstance(data, dict):
        # Convertir None a 'N/A' o 0 para evitar problemas en JS si no hay datos
        result = {k: (v if v is not None else 'N/A') for k, v in data.items()}
    elif isinstance(data, (list, tuple)) and len(data) >= 4:
        result = {
            'avg_sleep': data[0] if data[0] is not None else 'N/A',
            'avg_activity': data[1] if data[1] is not None else 'N/A',
            'avg_notifications': data[2] if data[2] is not None else 'N/A',
            'avg_tech_savviness': data[3] if data[3] is not None else 'N/A'
        }
    else: # Si no hay datos, devolver N/A
         result = {'avg_sleep': 'N/A', 'avg_activity': 'N/A', 'avg_notifications': 'N/A', 'avg_tech_savviness': 'N/A'}

    return JsonResponse(result)

# ELIMINAR o COMENTAR esta función:
# def country_age_gender_mix(request, country_id): ...

# ELIMINAR o COMENTAR esta función:
# def country_time_allocation(request, country_id): ...

# views.py (AÑADIR/MODIFICAR estas vistas API, puedes comentar/eliminar las 'gender_' anteriores si ya no se usan directamente)

def gender_platform_preference(request, gender_id):
    """Plataforma Social Primaria y Plataforma Preferida para Entretenimiento para este género."""
    # Query para plataforma SM primaria
    query_sm = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count
        FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.gender_id = %s
        GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    # Query para plataforma preferida para entretenimiento
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
    """Gasto promedio en entretenimiento agrupado por rangos de ingreso para este género."""
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
                'backgroundColor': 'rgba(255, 159, 64, 0.7)', # Naranja
                'borderColor': 'rgba(255, 159, 64, 1)',
                'yAxisID': 'y_spending',
                'borderWidth': 1,
                'type': 'bar'
            },
            {
                'label': 'Número de Usuarios', # Dataset opcional para contexto
                'data': [row.get('user_count', 0) for row in data],
                'backgroundColor': 'rgba(201, 203, 207, 0.5)', # Gris
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
    """Distribución del objetivo principal de uso de SM para este género."""
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
    """Indicadores promedio de engagement digital para este género."""
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

# --- Vistas API Reutilizadas/Existentes (Asegúrate que existan) ---
# gender_top_entertainment(request, gender_id)
# gender_sm_vs_ent_time(request, gender_id)
# gender_top_occupations(request, gender_id)

# Vista principal del detalle de género (sin cambios necesarios)
# def genderDetail(request, id): ... (ya la tienes)

# views.py (AÑADIR estas nuevas vistas API, puedes comentar/eliminar las 'ent_' anteriores si ya no se usan directamente)

def ent_core_demographics(request, entertainment_id):
    """Distribución de Edad y Género para quienes prefieren este entretenimiento."""
    # Edad
    query_age = """
        SELECT CASE
            WHEN u.age BETWEEN 0 AND 17 THEN '0-17' WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
            WHEN u.age BETWEEN 26 AND 35 THEN '26-35' WHEN u.age BETWEEN 36 AND 50 THEN '36-50' ELSE '51+'
            END AS age_group, COUNT(u.user_id) AS count
        FROM users u WHERE u.preferred_content_id = %s GROUP BY age_group ORDER BY age_group;
    """
    # Género
    query_gender = """
        SELECT g.gender, COUNT(u.user_id) AS count
        FROM users u JOIN gender g ON u.gender_id = g.gender_id
        WHERE u.preferred_content_id = %s GROUP BY g.gender ORDER BY count DESC;
    """
    data_age = execute_query(query_age, [entertainment_id])
    data_gender = execute_query(query_gender, [entertainment_id])
    if not isinstance(data_age, list): data_age = []
    if not isinstance(data_gender, list): data_gender = []

    # Ordenar age_data si es necesario (similar a como hicimos antes)
    age_order = {'0-17': 1, '18-25': 2, '26-35': 3, '36-50': 4, '51+': 5}
    data_age.sort(key=lambda x: age_order.get(x.get('age_group', ''), 99))


    chart_data = {
        'age_distribution': {'labels': [r.get('age_group') for r in data_age], 'data': [r.get('count') for r in data_age]},
        'gender_distribution': {'labels': [r.get('gender') for r in data_gender], 'data': [r.get('count') for r in data_gender]}
    }
    return JsonResponse(chart_data)

def ent_socioeconomic_profile(request, entertainment_id):
    """Perfil socioeconómico: Top Países, Top Ocupaciones, Distribución Ingresos."""
    # Top Países
    query_countries = """
        SELECT c.country_name, COUNT(u.user_id) AS count FROM users u
        JOIN countries c ON u.country_id = c.country_id
        WHERE u.preferred_content_id = %s GROUP BY c.country_name ORDER BY count DESC LIMIT 5;
    """
    # Top Ocupaciones
    query_occ = """
        SELECT o.occupation_name, COUNT(u.user_id) AS count FROM users u
        JOIN occupations o ON u.occupation_id = o.occupation_id
        WHERE u.preferred_content_id = %s GROUP BY o.occupation_name ORDER BY count DESC LIMIT 7;
    """
    # Distribución Ingresos
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
    """Plataformas (SM y Entretenimiento) y Dispositivos usados por esta audiencia."""
    # SM Primaria
    query_sm_plat = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
        JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    # Plataforma Entretenimiento Preferida
    query_ent_plat = """
        SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
        JOIN social_media sm ON u.preferred_enter_plat_id = sm.socialm_id
        WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;
    """
    # Dispositivo Entretenimiento
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
    """Perfil de Engagement: Comparación tiempo, Meta SM, Suscripciones, Estilo Vida."""
    # Tiempo Promedio
    query_time = "SELECT ROUND(AVG(d_entertain_time), 1) AS avg_ent, ROUND(AVG(d_sm_time), 1) AS avg_sm FROM users WHERE preferred_content_id = %s;"
    # Meta SM
    query_goal = """
        SELECT mg.goal_name, COUNT(u.user_id) AS count FROM users u JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
        WHERE u.preferred_content_id = %s GROUP BY mg.goal_name ORDER BY count DESC; """
    # Indicadores Lifestyle + Suscripciones
    query_life = """
        SELECT ROUND(AVG(subscription_plats),1) AS avg_subs, ROUND(AVG(avg_sleep_time),1) AS avg_sleep,
               ROUND(AVG(physical_activity_tiem),1) AS avg_activity, ROUND(AVG(tech_savviness_level),1) AS avg_tech
        FROM users WHERE preferred_content_id = %s; """

    data_time = execute_query(query_time, [entertainment_id])
    data_goal = execute_query(query_goal, [entertainment_id])
    data_life = execute_query(query_life, [entertainment_id])
    if not isinstance(data_goal, list): data_goal = []

    # Procesar tiempo
    time_labels = ['Tiempo Entretenimiento', 'Tiempo Redes Sociales']
    time_data = [0, 0]
    if isinstance(data_time, dict): time_data = [data_time.get('avg_ent', 0), data_time.get('avg_sm', 0)]
    elif isinstance(data_time, tuple): time_data = [data_time[0] if data_time[0] else 0, data_time[1] if data_time[1] else 0]

    # Procesar lifestyle
    life_indicators = {'avg_subs':'N/A', 'avg_sleep': 'N/A', 'avg_activity': 'N/A', 'avg_tech': 'N/A'}
    if isinstance(data_life, dict): life_indicators = {k: (v if v is not None else 'N/A') for k, v in data_life.items()}
    elif isinstance(data_life, tuple): life_indicators = {'avg_subs': data_life[0] if data_life[0] else 'N/A', 'avg_sleep': data_life[1] if data_life[1] else 'N/A', 'avg_activity': data_life[2] if data_life[2] else 'N/A', 'avg_tech': data_life[3] if data_life[3] else 'N/A'}

    chart_data = {
        'time_comparison': {'labels': time_labels, 'data': time_data},
        'sm_goal': {'labels': [r.get('goal_name') for r in data_goal], 'data': [r.get('count') for r in data_goal]},
        'lifestyle_and_subs': life_indicators # Combina indicadores en una sola respuesta
    }
    return JsonResponse(chart_data)


# Vista principal (sin cambios necesarios)
# def entertainmentDetail(request, id): ...

# sm_ads/views.py


def dictfetchall(cursor):
    """Devuelve todas las filas de un cursor como un diccionario."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados como lista de diccionarios."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return dictfetchall(cursor)
            else:
                # Para queries como COUNT(*) o AVG(*) que devuelven una sola fila/columna
                result = cursor.fetchone()
                # Si devuelve algo, intentar crear un diccionario simple si es posible
                if result and cursor.description:
                     # Re-ejecutar para obtener descripción (si fetchone() la consumió)
                     cursor.execute(query, params)
                     columns = [col[0] for col in cursor.description]
                     return [dict(zip(columns, result))] # Devolver como lista de 1 dict
                elif result:
                    # Si no hay descripción pero hay resultado (ej. COUNT(*))
                    return [{'result': result[0]}] # Devolver un dict genérico
                else:
                    return [] # Sin resultados
    except Exception as e:
        print(f"ERROR ejecutando query: {e}\nQuery: {query}\nParams: {params}")
        return [] # Devolver lista vacía en caso de error

def auxMenu():
    """Obtiene datos para los menús laterales."""
    redesSociales = SocialMedia.objects.all().order_by('socialm_name').values()
    paises = Countries.objects.all().order_by('country_name').values()
    generos = Gender.objects.all().order_by('gender').values()
    tipoEntretenimiento = Entretaiment.objects.all().order_by('entertainment_name').values()
    return redesSociales, paises, generos, tipoEntretenimiento

# --- Funciones para Métricas Principales (Usadas por la vista 'main') ---
# (Estas devuelven el valor directamente, no son APIs JSON)

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

# --- APIs para Gráficos de Contexto General ---

def get_top_platforms_distribution(request):
    """Distribución de plataformas sociales primarias."""
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
    """Distribución de preferencias de entretenimiento."""
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
    """Distribución de usuarios por país."""
    query = """
        SELECT c.country_name, COUNT(u.user_id) AS user_count
        FROM users u JOIN countries c ON u.country_id = c.country_id
        GROUP BY c.country_name ORDER BY user_count DESC LIMIT 10; -- Top 10
    """
    data = execute_query(query)
    chart_data = {
        'labels': [r.get('country_name', 'N/A') for r in data],
        'data': [r.get('user_count', 0) for r in data]
    }
    return JsonResponse(chart_data)

# --- APIs para "Datos Curiosos" ---

def get_platform_highest_avg_income(request):
    """Encuentra la plataforma social primaria con el ingreso promedio de usuario más alto."""
    query = """
        SELECT sm.socialm_name, ROUND(AVG(u.monthly_income), 2) AS avg_income
        FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
        GROUP BY sm.socialm_name
        HAVING COUNT(u.user_id) > 2 -- Mínimo 3 usuarios para considerar el promedio
        ORDER BY avg_income DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result) # Devuelve {'socialm_name': '...', 'avg_income': ...} o {}

def get_platform_for_highest_tech_savvy(request):
    """Encuentra la plataforma social primaria preferida por el grupo con mayor tech savviness."""
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
    return JsonResponse(result) # Devuelve {'socialm_name': '...', 'avg_tech': ...} o {}

def get_avg_subscriptions_per_income_bracket(request):
    """Calcula el promedio de suscripciones por rango de ingreso."""
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
    # Ordenar por bracket
    income_order = {'< $2000': 1, '$2k-$4k': 2, '$4k-$6k': 3, '$6k-$8k': 4, '$8k+': 5}
    data_filtered = [item for item in data if item.get('income_bracket') is not None]
    data_filtered.sort(key=lambda x: income_order.get(x.get('income_bracket', ''), 99))

    chart_data = {
        'labels': [r.get('income_bracket', 'N/A') for r in data_filtered],
        'data': [r.get('avg_subs', 0) for r in data_filtered]
    }
    return JsonResponse(chart_data) # Datos para gráfico de barras simple

def get_sleep_quality_by_notification_level(request):
    """Compara calidad de sueño promedio para usuarios con muchas vs pocas notificaciones."""
    # Definir umbral, ej. promedio de notificaciones
    avg_notif_query = "SELECT AVG(d_num_notifications) FROM users;"
    avg_notif_result = execute_query(avg_notif_query)
    threshold = avg_notif_result[0]['result'] if avg_notif_result and avg_notif_result[0].get('result') is not None else 50 # Default threshold

    query = f"""
        SELECT
            CASE WHEN d_num_notifications > {threshold} THEN 'Notificaciones Altas (> {int(threshold)})' ELSE 'Notificaciones Bajas (<= {int(threshold)})' END AS notif_level,
            ROUND(AVG(avg_sleep_time), 1) AS avg_sleep
        FROM users GROUP BY notif_level ORDER BY notif_level;
    """
    data = execute_query(query)
    result = {item.get('notif_level'): item.get('avg_sleep') for item in data}
    return JsonResponse(result) # Devuelve {'Notificaciones Altas...': 6.5, 'Notificaciones Bajas...': 7.1}

def get_sm_time_by_gaming_level(request):
    """Compara tiempo en SM promedio para usuarios con mucho vs poco tiempo de gaming."""
    # Umbral para "mucho" gaming, ej > 1 hora
    threshold = 1.0
    query = f"""
        SELECT
            CASE WHEN d_gaming_time > {threshold} THEN 'Gamers (> {threshold}h)' ELSE 'No/Poco Gamers (<= {threshold}h)' END AS gaming_level,
            ROUND(AVG(d_sm_time), 1) AS avg_sm_time
        FROM users GROUP BY gaming_level ORDER BY gaming_level;
    """
    data = execute_query(query)
    result = {item.get('gaming_level'): item.get('avg_sm_time') for item in data}
    return JsonResponse(result) # Devuelve {'Gamers...': 3.1, 'No/Poco Gamers...': 3.5}

def get_age_group_highest_ad_interaction(request):
    """Encuentra el grupo de edad con el mayor promedio de interacciones con anuncios."""
    query = """
        SELECT
             CASE WHEN age <= 17 THEN '0-17' WHEN age <= 25 THEN '18-25' WHEN age <= 35 THEN '26-35'
                  WHEN age <= 50 THEN '36-50' ELSE '51+' END AS age_group,
             ROUND(AVG(ad_interaction_count), 1) AS avg_interactions
        FROM users GROUP BY age_group ORDER BY avg_interactions DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result) # Devuelve {'age_group': '...', 'avg_interactions': ...} o {}

def get_occupation_distinct_entertainment(request):
    """Encuentra la ocupación con la preferencia de entretenimiento más 'distintiva' (rara)."""
    # Comparamos % de preferencia dentro de la ocupación vs % general
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
         WHERE ovp.overall_ratio > 0 AND toc.total_in_occ > 2 -- Mínimo 3 en la ocupación
         ORDER BY distinct_ratio DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result) # Devuelve {'occupation_name': '..', 'entertainment_name': '..', 'distinct_ratio': ..}

def get_country_highest_screen_time(request):
    """Encuentra el país con el mayor tiempo promedio de pantalla."""
    query = """
        SELECT c.country_name, ROUND(AVG(u.screen_time), 1) AS avg_screen_time
        FROM users u JOIN countries c ON u.country_id = c.country_id
        GROUP BY c.country_name HAVING COUNT(u.user_id) > 2
        ORDER BY avg_screen_time DESC LIMIT 1;
    """
    data = execute_query(query)
    result = data[0] if data else {}
    return JsonResponse(result) # Devuelve {'country_name': '...', 'avg_screen_time': ...} o {}


# --- Vista Principal 'main' (Revisada) ---
def main(request):
    # Datos para los menús laterales
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()

    # Datos para las tarjetas de métricas principales
    # Llamamos a las funciones auxiliares directamente aquí
    context = {
        'redesSociales': redesSociales,
        'paises': paises,
        'generos': generos,
        'tipoEntretenimiento': tipoEntretenimiento,
        # --- Métricas Principales ---
        'total_users_metric' : get_total_users_count(),
        'avg_age_metric': get_avg_age_value(),
        'avg_income_metric': get_avg_income_value(),
    }

    template = loader.get_template('index.html') # Asegúrate que sea index.html
    return HttpResponse(template.render(context, request))


# --- Vistas de Detalle (No las modificamos ahora, pero asegúrate que existan) ---
def socialMediaPlatform(request, id):
    # ... (tu código existente para smp.html)
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    platform = SocialMedia.objects.get(pk=id)
    context = {'platform_id': id, 'platform_name': platform.socialm_name, 'titulo': platform.socialm_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('smp.html')
    return HttpResponse(template.render(context, request))

def countriesDetail(request, id):
    # ... (tu código existente para paises.html)
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    country = Countries.objects.get(pk=id)
    context = {'country_id': id, 'country_name': country.country_name, 'titulo': country.country_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('paises.html')
    return HttpResponse(template.render(context, request))

def genderDetail(request, id):
    # ... (tu código existente para generos.html)
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    gender = Gender.objects.get(pk=id)
    context = {'gender_id': id, 'gender_name': gender.gender, 'titulo': gender.gender.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('generos.html')
    return HttpResponse(template.render(context, request))

def entertainmentDetail(request, id):
     # ... (tu código existente para entretenimiento.html)
    redesSociales, paises, generos, tipoEntretenimiento = auxMenu()
    entertainment = Entretaiment.objects.get(pk=id)
    context = {'entertainment_id': id, 'entertainment_name': entertainment.entertainment_name, 'titulo': entertainment.entertainment_name.upper(), 'redesSociales': redesSociales, 'paises': paises, 'generos': generos, 'tipoEntretenimiento': tipoEntretenimiento}
    template = loader.get_template('entretenimiento.html')
    return HttpResponse(template.render(context, request))

# ... (Otras vistas API que usan las páginas de detalle, si las tienes separadas)