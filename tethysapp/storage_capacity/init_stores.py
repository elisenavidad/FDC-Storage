# Put your persistent store initializer functions in here
from .model import engine, SessionMaker, Base, FlowDurationData

def init_fdc_db(request):
	"""
	Initializer for fdc database
	"""
	#Create table from gp service
	Base.metadata.create_all(engine)

	if 'results' in request.POST['app.submitResRequest()']:
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


