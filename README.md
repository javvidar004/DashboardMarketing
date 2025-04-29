# DashboardMarketing
Objetivo: Generar un Dashboard para elección de donde publicar publicidad según el cliente objetivo   
Dataset: Obtained from Kaggle, social media use

## Tabla de contenido
1. [Introduccion](#introduccion)
2. [Informacion general](#Informacion-general)
3. [¿Como ejecutar el proyecto?](#¿Como-ejecutar-el-proyecto?)   
	a. [La primera vez ejecutando el proyecto](#La_primera_vez_ejecutando_el_proyecto)   
	b. [Cada vez que se vaya a ejecutar el proyecto](#Cada_vez_que_se_vaya_a_ejecutar_el_proyecto)   
5. [Estructura del proyecto](#Estructura-del-proyecto)    
	a. [Carpetas](#carpetas)   
	b. [Views, URLs, Models](#Views,-URLs,-Models)   
	c. [Estructura de la BD](#Estructura-de-la-BD)   
	d. [Conexion de BD a DJango](#Conexion-de-BD-a-DJango)   
	e. [WhiteNoise para CSS y JS](#WhiteNoise-para-CSS-y-JS)   
	f. [Queries de Servicio](#Queries-de-Servicio)   
	g. [Creacion de Graficas](#Creacion-de-Graficas)   
6. [Conclusiones](#conclusiones)
### Introduccion

***
### Informacion general
El proyecto esta construido a partir del proyecto de generar un Dashboard conectando Frontend con Backend. Debido a la simplicidad de concetar la base de datos con el Frontend utilizamos Django basado en python para generar la conexion asi como toda la estructura de la pagina WEB. Para fines de pryecto y de la simplicidad de la produccion se obtuvo una plantilla con documentos HTML, CSS y JS. Simplemente hubo que adapatarlo a las preferencias del proyecto asi como a la forma de trabajar con Django ya que la estructura de carpetas para el proyecto debe seguir una estructura especifica.
***

## ¿Como ejecutar el proyecto?
Primero descarga el proyecto. Segundo entra a CMD o lineas de comandos, de ahi viaja por las carpetas hasta encontrarte en el directorio de la carpeta del proyecto, donde si ejecutas el comando dir(en Windows) o ls(en linux o Mac) debe aparecer el archivo manage.py junto con las carpetas: marketing_dashboard, productionfiles y sm_ads.
Una vez en el directorio se debe ejectuar los siguientes comandos.  
### La primera vez ejecutando el proyecto
Para Windows:  
```CMD
py -m venv dashboardenv
```
Se debe entrar a la carpeta 
```CMD
cd dashboardenv
```
```CMD
cd Scripts
```
```CMD
activate.bat
```
Para Mac:  
```CMD
python3 -m venv dashboardenv
```
Se debe entrar a la carpeta 
```CMD
source bin/activate
```
Después se debe regresar al directorio del inicio, se puede regresar al directorio con el siguiente comando ejecutado dos veces:
```CMD
cd..
```
Una vez estando de vuelta en el dirctorio se debe ejecutar el siguiente comando:
```CMD
pip install -r requirements.txt
```
ejecutar la siguiente linea de codigo:
Para poder ejecutar el siguiente comando ya es necesario tener activo el servidor con la base de datos, ya que se haran ciertas modificaciones a la base de datos.
```CMD
py manage.py makemigrations sm_ads
```
```CMD
py manage.py migrate
```
Para el siguiente comando te preguntará si quieres remplazar los documentos anteriores a lo que se contesta con 'Y' y continua el proceso para poder ejecutar el servido.
```CMD
py manage.py collectstatic
```

### Cada vez que se vaya a ejecutar el proyecto
Como consideracion adicional hay que tener en cuenta que se debe tener corriendo el servido en MySQL con la base de datos con nombre socialmediause.  
Además configurar en el documento settings.py en 'DATABASES', asegurarse que el 'NAME', 'USER', 'PASSWORD' concuerden con el nombre de la base de datos, el USER con el usuario de MySQL y la contraseña del usuario.
```CMD
py manage.py runserver
```

Para Linux:  
En caso de no tener instalado python se deben instalar los siguientes paquetes:
```CMD
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3.12-venv
```
Crear el ambiente virtual con los mudlos necesarios para ejecutar el proyecto  
```CMD
python3 -m venv dashboardenv
```
Se debe entrar a la carpeta 
```CMD
cd dashboardenv/bin
source ./activate
```

Después se debe regresar al directorio del inicio, se puede regresar al directorio con el siguiente comando ejecutado dos veces:
```CMD
cd..
```
Una vez estando de vuelta en el dirctorio se debe ejecutar el siguiente comando:
```CMD
pip install -r requirements.txt
```
En caso de no poder intalar mysqlclient, ejecutar el siguiente comando y volver a intentar:  
```CMD
sudo apt-get update && sudo apt-get install python3-dev default-libmysqlclient-dev
```

ejecutar la siguiente linea de codigo:
Para poder ejecutar el siguiente comando ya es necesario tener activo el servidor con la base de datos, ya que se haran ciertas modificaciones a la base de datos.

```CMD
python3 manage.py migrate
```
Para el siguiente comando te preguntará si quieres remplazar los documentos anteriores a lo que se contesta con 'Y' y continua el proceso para poder ejecutar el servido.
```CMD
python3 manage.py collectstatic
```

### Cada vez que se vaya a ejecutar el proyecto
Como consideracion adicional hay que tener en cuenta que se debe tener corriendo el servido en MySQL con la base de datos con nombre socialmediause.  
Además configurar en el documento settings.py en 'DATABASES', asegurarse que el 'NAME', 'USER', 'PASSWORD' concuerden con el nombre de la base de datos, el USER con el usuario de MySQL y la contraseña del usuario.
```CMD
py manage.py runserver
```


## Estructura del proyecto
#### carpetas
El proyecto esta estructurado en 3 carpetas principales:
1. marketing_dashboard: Esta capeta es la principal del proyecto al cearla con Django. En esta se encuentran los documentos principales de la configuracion del proyecto. Los dos principales documentos de esta carpeta para ajustar el proyecto a los requisitos es el documento settings.py y urls.py. Los demas documentos son necesarios para el funcionamiento, sin embargo, en este proyecto nos interresan mas los otros documentos.
2. productionfiles: Esta carpeta almacena todos los archivos CSS y JS necesarios para el funcionamiento y estilizado en la ejecucuion del servidor para la visualizacion de la pagina. Para mayor entendimiento de esta carpeta vease el punto e de carpetas.
3. sm_ads: Esta carpeta cumple con el funcionamiento de ser la app de Django dentro del proyecto. Dentro de esta carpeta se almacena todo lo referente a la ejecucion y funcionamiento en cuanto a los urls de la pagina web asi como documentos HTML y todo lo relacionado con la ejecucion de codigo python dentro de los documentos HTML. Tambien como es que se reciben y se pasan datos de la base de datos al Frontend.
##### Documentos adicionales
service_queries es documento donde se almacenan los queries de servicio para mostrar los datos relevantes en la pagina.   
manage.py es documento utilizado para la ejecucion, modificacion y recopilacion de diferentes documentos asi como modificaciones en el proyecto.   
requirements es el documento donde se almacenan los modulos que se requieren en el venv para poder ejecutar el proyecto sin errores.   

#### Views, URLs, Models
##### Models:
El documento Models almacena los modelos de la aplicacion. Estos se construyen a partir de la base de datos, cada modelo representa un registro de cada una de las tablas distintas. Por lo que si se analiza a detalle cada uno de los modelos es el diccionario completo de la base de datos.   
Este documento ya no es necesario modificar en caso de ser necesario habria que cambiar algo en la base de datos.  
##### Views:
En View se encuentran las funciones que se ejecutan detrás de cada uno de los URLs que se llaman cuando es en ejecucion el servidor.  
Dentro de cada funcion primero se debe otener el template que es el documento HTML a partir del cual se estructurara la pagina.
```python
template = loader.get_template('<NOMBRE DEL DOCUMENTO>.html')
```
Despues se tiene la linea de codigo para ejecutar el query a la base de datos para que de esta manera, se puedan usar los datos obtenidas en la visualizacion de la pagina.  
Cabe resaltar que dentro del select se tiene que mantener la llave primaria del modelo, por lo que se pueden ejecutar queries pero siempre con la restriccion de mantener la llave primaria. De esta manera se ejecutaran los queries de servicio.  
```python
variable = Nombre_Modelo.objects.raw("query")
```
Tras obtener los datos de la base, se deben pasar de la siguiente manera en context que serán todos los datos que se pueden utilizar dentro de la pagina WEB.

```python
context = {
    'nombre': variable,
    'nombre2': variable2,
    ...
  }
```
Se pueden pasar tantos datos como sena necesarios al context, asi como tambien se pueden ejecutar la cantidad de consultas necesarias a la base de datos.   
Por ultimo se ejecuta el return, aqui se pasan tanto los datos como el template para que se ejecute el URL
```python
return HttpResponse(template.render(context, request))
```

##### URLs:
En URLs basicamente decides que urls tendra tu pagina web, por lo que si implementas hipervinculos de una pagina a otra es necesario agregar los links que se generan en URLs pues de ser contrario, generara un error, puede ser que no abra nada o en caso de tener documento 404.html, se ejecutara ese error anunciando que no se ha encontrado el recurso al que se dirigio.  
En el documento se tiene la siguiente estructura :  

```python
urlpatterns = [
    path('', views.main, name='main'),
    path('index.html', views.main, name='main'),
    path('general.html', views.general, name='general'),
    path('get_chart1/', views.get_chart1, name='get_chart1'),
    ...
]
```
El primer parametro hace a la referencia del link al que uno se dirige y que aparece a lado del dominio como parte de la ruta. El segundo parametro se nombra que funcion del documento view se usara para esa ruta, por ultimo el nombre es un nombre de referencia, por lo que se podria omitir.  
Es importante resaltar que en este caso no se utiliza, sin embargo, hay una funcion con la que se pueden pasar valores por la direccion lo que permite hacer paginas personalizadas para cada usuario segun su ID.   
Para mas informacion sobre la estructura y creacion de recursos en django [da clic aqui](https://docs.djangoproject.com/en/5.1/)      
#### Estructura de la BD
  
| TABLE: countries | TABLE: devices | TABLE: entretaiment  | TABLE: gender | TABLE: media_goal | TABLE: occupations | TABLE: social_media | 
|------------------|----------------|----------------------|---------------|-------------------|--------------------|---------------------|
|-country_id       | -device_id     | -entertainment_id    | -gender_id    | -goal_id          | -occupation_id     | -socialm_id         |
|-country_name     | -device_name   | -entertainment_name  | -gender       | -goal_name        | -occupation_name   | -socialm_name       |

##### TABLE: users
| CAMPO    | SIGNIFICADO/CONEXION |
|----------|----------------------|
|-user_id  ||
|-age      ||
|-gender_id| (foreign index from gender table)   |
|-country_id| (foreign index from gender table)  |
|-d_sm_time |(daily social media time)  |
|-d_entertain_time| (daily entertainment time)  |
|-sm_plat_used| (number of social media platforms used)  |
|-primary_plat_id| (foreign index from social_media table)  |
|-d_message_time| (daily messaging time)  |
|-d_vid_cont_time| (daily video content time)  |
|-d_gaming_time| (daily gaming time)  |
|-occupation_id| (foreign index from occupations table)  |
|-monthly_income|  |
|-device_sm_id| (foreign index from devices table)  |
|-subscription_plats| (number of susbscription in platforms)  |
|-avg_sleep_time | |
|-physical_activity_time|  |
|-reading_time ||
|-work_study_time||  
|-screen_time | |
|-d_num_notifications| (notifications recibed daily)  |
|-d_music_time| (daily music time)  |
|-preferred_content_id| (foreign index from entretaiment table)|
|-primary_sm_goal_id| (foreign index from media_goal table)  |
|-preferred_enter_plat_id| (foreign index from social_media table)  |
|-online_comm_time| (Time spent in online communities)  |
|-news_time| (news consumption time)  |
|-ad_interaction_count|  |
|-education_plat_time| (education platform time)  |
|-tech_savviness_level|  |
|-devide_for_entertainment_id| (foreign index from devices table)   |
|-sleep_quality | |
|-monthly_spent_entertain| |  
#### Conexion de BD a DJango


#### WhiteNoise para CSS y JS


#### Queries de Servicio

```SQL
SELECT * FROM *;
```

#### Creacion de Graficas



## Conclusiones
Esta quedando muy bonito

