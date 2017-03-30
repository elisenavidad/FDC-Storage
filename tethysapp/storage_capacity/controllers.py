from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import TableView, LinePlot

from .model import SessionMaker, FlowDurationData

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
	session=SessionMaker()
	fdcDataQuery=session.query(FlowDurationData)
	if 'results' in request.POST['app.stores']:
		with open(results,'r') as f:
			lines=f.read().splitlines()

		lines.pop(0)
		session=SessionMaker()

		for line in lines:
			row=line.split(',')
			fdc_row=fdcData(
				percent=row[0],
				flow=row[1],
				units='m^3/s'
				)

			session.add(fdc_row)
		session.commit()
		session.close()

	print session
	fdc_tbv=TableView(column_names=('Percent (%)', unicode('Flow (m'+u'\u00b3'+'/s)')),
					rows=fdcDataQuery,
					hover=True,
					striped=True,
					bordered=True,
					condensed=True,
					editable_columns=(False,False,False),
					row_ids=[range(0,3)]
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
			'data': fdcDataQuery

		}]

		)



	context={'fdc_tbv':fdc_tbv,
			'plot_view':plot_view}
	return render(request, 'storage_capacity/resultspage.html',context)