from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def index(request):

    template = loader.get_template('tripous/index.html')

    # initialize dummy values
    context = {"stock_name":"See the requested graph here",
                "graph_src":"dummy.png",
                # alert-success|alert-info|alert-warning|alert-danger -- | hidden
                "alert_class":"hidden",
                "alert_text":"",
                }


    return HttpResponse(template.render(context,request))
