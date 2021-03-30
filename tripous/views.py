from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import loader



# Import custom Logic
from . import yFinance as yFin
from . import visualization as vis
from . import prediction as pred


def index(request):
    template = loader.get_template('tripous/index.html')

    # initialize dummy values
    context = {"stock_name":"See the requested graph here",
                "graph_html":"""<div id="graphWrapper" class="graph" style="background-image:url('/static/tripous/img/graph/dummy.png')"></div>""",
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
            
        context["stock_name"] = info["longName"]

        # predict Stuff
        predDF = pred.predictDF(df)

        # visualize stuff
        context["graph_html"] = vis.getHTMLFromPlotly(predDF, info, plotTimeframe=180)
    

    # send all data to the frontend
    # if no search request has been sent, just return default values 
    return HttpResponse(template.render(context,request))
