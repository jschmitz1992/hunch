from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import loader



# Import custom Logic
from . import yFinance as yFin
from . import visualization as vis


def index(request):
    template = loader.get_template('tripous/index.html')

    # initialize dummy values
    context = {"stock_name":"See the requested graph here",
                "graph_src":"dummy.png",
                # alert-success|alert-info|alert-warning|alert-danger -- | hidden
                "alert_class":"hidden",
                "alert_text":"",
                }





    # get params
    sQuery = request.GET.get('search', None)
    # TODO: Validate search query

    if sQuery is not None:
        # try to get data
        try:
            df, info = yFin.getDFOfSymbol(sQuery)

        except AssertionError:   
            # for 404
            context["alert_class"] = "alert-info"
            context["alert_text"] = "The stock you are looking for could not be found, please type in another one."
            return HttpResponse(template.render(context,request))
            
        except Exception:
            # for 500, 429 or else
            context["alert_class"] = "alert-danger"
            context["alert_text"] = "This service is currentyl unavailable, please try again in a few minutes."
            return HttpResponse(template.render(context,request))
            

        context["graph_src"] = vis.plotOfDF(df,info)
        context["stock_name"] = info["longName"]



    return HttpResponse(template.render(context,request))
