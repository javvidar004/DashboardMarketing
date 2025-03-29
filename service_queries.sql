SELECT entretaiment.entertainment_id, entretaiment.entertainment_name, COUNT(preferred_content_id) AS people FROM entretaiment, users WHERE preferred_content_id = entretaiment.entertainment_id GROUP BY entretaiment.entertainment_id;
//Muestra el tipo de entretenimiento que prefiere la gente


SELECT entretaiment.entertainment_id, entretaiment.entertainment_name, COUNT(preferred_content_id) AS people 
FROM entretaiment, users, countries
WHERE preferred_content_id = entretaiment.entertainment_id AND
	countries.country_id = 1 AND
    countries.country_id = users.country_id
GROUP BY entretaiment.entertainment_id;
//Muestra el tipo de entretenimiento preferido por pais
//Se puede usar un ciclo for cambiar el "countries.country_id = 1" para en el valor obtener todos los datos con todos los paises


SELECT countries.country_id, countries.country_name, COUNT(preferred_content_id) AS people 
FROM entretaiment, users, countries
WHERE preferred_content_id = entretaiment.entertainment_id AND
	entretaiment.entertainment_id = 1 AND
    countries.country_id = users.country_id
GROUP BY countries.country_id;
//Muestra el numero de preferencia de un tipo de entretenimiento por pais
//Se puede usar un ciclo for cambiar el "entretaiment.entertainment_id = 1" para en el valor obtener todos los datos con todos los tipos de entretenimiento


//pais que mas gasta en entretenimiento
SELECT 
    countries.country_id,
    countries.country_name,
    SUM(users.monthly_spent_entertain) AS total_spent
FROM 
    users
JOIN 
    countries ON users.country_id = countries.country_id
GROUP BY 
    countries.country_id, countries.country_name
ORDER BY 
    total_spent DESC;



//pais que mas gana
SELECT 
    countries.country_id,
    countries.country_name,
    AVG(users.monthly_income) AS avg_income
FROM 
    users
JOIN 
    countries ON users.country_id = countries.country_id
GROUP BY 
    countries.country_id, countries.country_name
ORDER BY 
    avg_income DESC;



//Usuarios por grupo de edad, red social y país
SELECT 
    countries.country_name,
    social_media.socialm_name,
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
GROUP BY countries.country_name, social_media.socialm_name, age_group
ORDER BY countries.country_name, social_media.socialm_name, total_users DESC;




//Genero que mas usa cada red social por pais
SELECT 
    countries.country_name,
    social_media.socialm_name,
    gender.gender,
    COUNT(*) AS total_users
FROM users
JOIN countries ON users.country_id = countries.country_id
JOIN social_media ON users.primary_plat_id = social_media.socialm_id
JOIN gender ON users.gender_id = gender.gender_id
GROUP BY countries.country_name, social_media.socialm_name, gender.gender
ORDER BY countries.country_name, social_media.socialm_name, total_users DESC;



//relacion entre la ocupacion de la persona y su red social mas usada
SELECT 
  occupations.occupation_name,
  social_media.socialm_name,
  COUNT(*) AS total_users
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
JOIN social_media ON users.primary_plat_id = social_media.socialm_id
GROUP BY occupations.occupation_name, social_media.socialm_name
ORDER BY occupations.occupation_name, total_users DESC;



//gasto en redes segun la ocupacion
SELECT 
    occupations.occupation_name,
    SUM(users.monthly_spent_entertain) AS total_spent
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
GROUP BY occupations.occupation_name
ORDER BY total_spent DESC;



//Objetivo de redes sociales por ocupacion
SELECT 
    occupations.occupation_name,
    media_goal.goal_name,
    COUNT(*) AS total_users
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
JOIN media_goal ON users.primary_sm_goal_id = media_goal.goal_id
GROUP BY occupations.occupation_name, media_goal.goal_name
ORDER BY occupations.occupation_name, total_users DESC;



//Dispositivos en los que mas se consume redes sociales
SELECT 
    devices.device_name,
    COUNT(*) AS total_users
FROM users
JOIN devices ON users.device_sm_id = devices.device_id
GROUP BY devices.device_name
ORDER BY total_users DESC;

//Dispositivos en los que mas se consume entretenimiento
SELECT 
    devices.device_name,
    COUNT(*) AS total_users
FROM users
JOIN devices ON users.devide_for_entertainment_id = devices.device_id
GROUP BY devices.device_name
ORDER BY total_users DESC;


// Relación que existe entre los ingresos y los gastos en cosas de entretenimiento 

SELECT country_name, AVG(users.monthly_income) AS prom_ingresos, AVG(users.monthly_spent_entertain) AS prom_gastos
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY country_name
ORDER BY prom_gastos DESC;

// Para saber en que países pasan más tiempo entre redes sociales o plataformas de entretenimiento:

SELECT countries.country_name, AVG(users.d_sm_time) AS prom_redes_sociales, AVG(users.d_entertain_time) AS prom_plat_entret
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY countries.country_name
ORDER BY prom_redes_sociales DESC;

// Redes sociales más usadas por las personas dependiendo de a que se dedican:

SELECT occupations.occupation_name, social_media.socialm_name,
COUNT(users.user_id) AS total_usuarios
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
JOIN social_media ON users.primary_plat_id = social_media.socialm_id
GROUP BY occupations.occupation_name, social_media.socialm_name
ORDER BY total_usuarios DESC;

// Tiempo frente a la pantalla relacionado con la calidad de sueño de las personas:

SELECT 
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
ORDER BY users_count DESC;
