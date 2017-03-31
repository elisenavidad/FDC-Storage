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
	fdcData=cgi.FieldStorage()


	fdc_tbv=TableView(column_names=('Percent (%)', unicode('Flow (m'+u'\u00b3'+'/s)')),
					rows=[(99, 2.65),(95,7.67),(90,9.02),(85,10.35),(75,12.19),(70,13.31),(60,13.33),(50,18.59),(40,19.01),(30,24.62),(20,33.32)],
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
			'data': [
					[99,2.65],[95,7.67],[90,9.02],[85,10.35],[75,12.19],[70,13.31],[60,13.33],[50,18.59],[40,19.01],[30,24.62],[20,33.32]]

		}]

		)



	context={'fdc_tbv':fdc_tbv,
			'plot_view':plot_view}
	return render(request, 'storage_capacity/resultspage.html',context)