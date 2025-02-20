# DashboardMarketing
Objetivo: Generar un Dashboard para elección de donde publicar publicidad según el cliente objetivo   
Dataset: Obtained from Kaggle, social media use

## Tabla de contenido
1. [Introduccion](#introduccion)
2. [Informacion general](#Informacion-general)
3. [¿Como ejecutar el proyecto?](#¿Como-ejecutar-el-proyecto?)
	a. [La primera vez ejecutando el proyecto:](#La_primera_vez_ejecutando_el_proyecto:)
	b. [Cada vez que se vaya a ejecutar el proyecto:](#Cada_vez_que_se_vaya_a_ejecutar_el_proyecto:)
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
### La primera vez ejecutando el proyecto:  
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
Después se debe regresar al directorio del inicio, se puede regresar al directorio con el siguiente comando ejecutado dos veces:
```CMD
cd..
```
Una vez estando de vuelta en el dirctorio se debe ejecutar el siguiente comando:
```CMD
pip install -r requirements.txt
```
ejecutar la siguiente linea de codigo:
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

### Cada vez que se vaya a ejecutar el proyecto:  
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

```python
print("Hello, World!")
```
#### Estructura de la BD


#### Conexion de BD a DJango


#### WhiteNoise para CSS y JS


#### Queries de Servicio

```SQL
SELECT * FROM *;
```

#### Creacion de Graficas



## Conclusiones
Esta quedando muy bonito

