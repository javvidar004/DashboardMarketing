# DashboardMarketing
Objetivo: Generar un Dashboard para elección de donde publicar publicidad según el cliente objetivo
Dataset: Obtained from Kaggle, social media use

## Tabla de contenido
1. [Introduccion](#introduccion)
2. [Informacion general](#Informacion-general)
3. [Estructura del proyecto](#Estructura-del-proyecto)
	a. [Carpetas](#carpetas)
  b. [Views, URLs, Models](#Views,-URLs,-Models)
  c. [Estructura de la BD](#Estructura-de-la-BD)
	d. [Conexion de BD a DJango](#Conexion-de-BD-a-DJango)
	e. [WhiteNoise para CSS y JS](#WhiteNoise-para-CSS-y-JS)
	f. [Queries de Servicio](#Queries-de-Servicio)
  g. [Creacion de Graficas](#Creacion-de-Graficas)
5. [¿Como ejecutar el proyecto?](#¿Como-ejecutar-el-proyecto?)
6. [Conclusiones](#conclusiones)
### Introduccion

***
### Informacion general
El proyecto esta construido a partir del proyecto de generar un Dashboard conectando Frontend con Backend. Debido a la simplicidad de concetar la base de datos con el Frontend utilizamos Django basado en python para generar la conexion asi como toda la estructura de la pagina WEB. Para fines de pryecto y de la simplicidad de la produccion se obtuvo una plantilla con documentos HTML, CSS y JS. Simplemente hubo que adapatarlo a las preferencias del proyecto asi como a la forma de trabajar con Django ya que la estructura de carpetas para el proyecto debe seguir una estructura especifica.
***
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



## ¿Como ejecutar el proyecto?

```CMD
py manage.py runserver
```

## Conclusiones
Esta quedando muy bonito

