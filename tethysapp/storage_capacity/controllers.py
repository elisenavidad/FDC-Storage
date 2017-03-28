from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'storage_capacity/home.html', context)

def results(request):
	"""
	Controller for the app results page.
	"""
	context={}
	return render(request, 'storage_capacity/results.html',context)