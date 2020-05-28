from django.shortcuts import render
from .models import Guider
from .forms import DateForm, SiteForm
# Create your views here.
from django.utils.timezone import now
from datetime import datetime 

def guider_images(request):


	if request.method == "POST":
		search_date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
		search_site = request.POST['site']
	
	else:
		search_date = now()
		search_site = 'TLV'

	print(search_date)

	guider = Guider.objects.filter( obs_date__date=search_date ).filter(site__iexact=search_site)

	if guider.count() > 0:
		message = None

	else:
		message = 'No guider images found.\n Come back later!'

	context = {	'guider' 	: guider, 
				'DateForm' 	: DateForm( initial = {'date' : search_date.strftime('%m/%d/%Y') } ), 
				'SiteForm' 	: SiteForm( initial = {'site' : search_site} ),
				'message' 	: message }

	# Display all the posts
	return render(request, 'bullseye/images.html', context)