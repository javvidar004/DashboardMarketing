from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
from random import randrange
from .models import *


def main(request):
  prefEntre = Entretaiment.objects.raw('SELECT entretaiment.entertainment_id AS entertainment_id, entretaiment.entertainment_name AS name, COUNT(preferred_content_id) AS people FROM entretaiment, users WHERE preferred_content_id = entretaiment.entertainment_id GROUP BY entretaiment.entertainment_id;')
  redesSociales = SocialMedia.objects.all().values()
  paises = Countries.objects.all().values()
  generos = Gender.objects.all().values()
  tipoEntretenimiento = Entretaiment.objects.all().values()
  template = loader.get_template('index.html') 
  context = {
     'prefEntre' : prefEntre,
     'redesSociales': redesSociales,
     'paises': paises,
     'generos': generos,
     'tipoEntretenimiento': tipoEntretenimiento,
  }
  return HttpResponse(template.render(context, request))


  #path('smp/<int:id>', views.socialMediaPlatform, name=detailPlatform)
def socialMediaPlatform(request, id):
    template = loader.get_template()
    context = {

    }
    return HttpResponse(template.render(context, request))
  
  #path('cntr/<int:id>', views.countriesDetail, name=detailContry)
def countriesDetail(request, id):
    template = loader.get_template()
    context = {

    }
    return HttpResponse(template.render(context, request))

  #path('gnr/<int:id>', views.genderDetail, name=detailGender)
def genderDetail(request, id):
    template = loader.get_template()
    context = {

    }
    return HttpResponse(template.render(context, request))

  #path('entr/<int:id>', views.entertainmentDetail, name=detailEntertainment)
def entertainmentDetail(request, id):
    template = loader.get_template()
    context = {

    }
    return HttpResponse(template.render(context, request))


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
