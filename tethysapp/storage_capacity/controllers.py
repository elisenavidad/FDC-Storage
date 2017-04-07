from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import TableView, LinePlot

from .model import SessionMaker, FlowDurationData
import json, sys, cgi


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'storage_capacity/home.html', context)

def resultspage(request):
	"""
	Controller for the app results page.
	"""

	#Get fdc data from main.js file through GET function
	data=request.GET
	flowlist=data['key1']
	print flowlist
	#format flowlist, and split by ,
	flowlist=flowlist[1:-1]
	flowlist_list=flowlist.split(",")
	flow_float=[float(s.encode('ascii')) for s in flowlist_list]
	flow_format=['%.2f' % elem for elem in flow_float]
	#define percentages
	plist=[99,95,90,85,75,70,60,50,40,30,20]
	#zip lists together
	paired_lists=zip(plist,flow_format)
	print paired_lists
	#format for LinePlot
	plot_data=[[float(s) for s in list] for list in paired_lists]



	fdc_tbv=TableView(column_names=('Percent (%)', unicode('Flow (m'+u'\u00b3'+'/s)')),
					rows=paired_lists,
					hover=True,
					striped=True,
					bordered=True,
					condensed=True,
					editable_columns=(False,False,False),
					row_ids=[range(0,10)]
					)

	plot_view=LinePlot(
		height='100%',
		width='200px',
		engine='highcharts',
		title='Flow-Duration Curve',
		subtitle=' ',
		spline=True,
		x_axis_title='Percent',
		x_axis_units='%',
		y_axis_title='Flow',
		y_axis_units='m^3/s',
		series=[{
			'name': 'Flow',
			'color': '#0066ff',
			'marker': {'enabled':False},
			'data': plot_data
		}]

		)



	context={'fdc_tbv':fdc_tbv,
			'plot_view':plot_view}
	return render(request, 'storage_capacity/resultspage.html',context)