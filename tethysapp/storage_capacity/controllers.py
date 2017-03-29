from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import LinePlot


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



	plot_view=LinePlot(
		height='500px',
		width='500px',
		engine='d3',
		title='Flow-Duration Curve',
		subtitle='test',
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
				[0, 5], [10, -70],
               [20, -86.5], [30, -66.5],
               [40, -32.1],
               [50, -12.5], [60, -47.7],
               [70, -85.7], [80, -106.5]
               ]

		}]

		)



	context={'plot_view':plot_view}
	return render(request, 'storage_capacity/resultspage.html',context)