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


//pais que mas gana


//Sector de edad que mas usa cada red social por pais


//Genero que mas usa cada red social por pais


//relacion entre la ocupacion de la persona y su red social mas usada


//gasto en redes segun la ocupacion


//Objetivo de redes sociales por pais y por ocupacion


//Dispositivos en los que mas se consume redes sociales
//Dispositivos en los que mas se consume entretenimiento




