from astropy.io import fits as pf
import os
import glob
import imageio
import re
from astropy.time import Time
import numpy as np

from django.conf import settings
import django

from NRES.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from bullseye.models import *
import requests
import tempfile
import datetime

fmt_api = '%Y-%m-%d'
fmt_disk = '%Y%m%d'

dt1 = datetime.timedelta(days=1)


# Get data from user file:
fuser = open(os.environ['ARCHIVEDATA'] , 'r')
username = (fuser.readline().split('=')[-1]).split()[0]
password = (fuser.readline().split('=')[-1]).split()[0]
api_token = requests.post('https://archive-api.lco.global/api-token-auth/',data = {'username': username,'password': password}).json() 
headers={'Authorization': 'Token '+api_token['token']}  
url='https://archive-api.lco.global/frames/?'


outgif = '../guider_gifs/'

guiderc = {	'tlv' : 'ak10',
			'lsc' : 'ak01',
			'cpt' : 'ak05',
			'elp' : 'ak11',} #'ak04'

#check if archive is mounted




def bullseye(obsdate='20190125', site='tlv'):

	current_night = datetime.datetime.strptime(obsdate, fmt_disk)

	if site == 'cpt':
		sdate = current_night.strftime(fmt_api)     +' 11%3A30'
		edate = (current_night+dt1).strftime(fmt_api)+' 11%3A00'
	if site == 'elp':
		sdate = current_night.strftime(fmt_api)     +' 18%3A30'
		edate = (current_night+dt1).strftime(fmt_api)+' 18%3A00'
	if site == 'lsc':
		sdate = current_night.strftime(fmt_api)     +' 16%3A30'
		edate = (current_night+dt1).strftime(fmt_api)+' 16%3A00'
	if site == 'tlv':
		sdate = current_night.strftime(fmt_api)     +' 10%3A30'
		edate = (current_night+dt1).strftime(fmt_api)+' 10%3A00'

	response = requests.get(url+'start='+sdate+'&end='+edate+'&SITEID='+site+\
		'&OBSTYPE=GUIDE&basename=&RLEVEL=0&TELID=',headers=headers).json()

	frames = response['results']

	with tempfile.TemporaryDirectory() as temp_directory:
		for frame in frames:
			with open( os.path.join(temp_directory,frame['filename']) , 'wb') as ff:
				ff.write(requests.get(frame['url']).content)

		filelist= sorted( glob.glob( os.path.join(temp_directory,'*.fits.fz') ) )

		if len(filelist) > 0:

			year 	= obsdate[0:4]
			month 	= obsdate[4:6]
			day 	= obsdate[6:8]

			if not os.path.isdir( os.path.join(outgif,year) ):
				os.mkdir( os.path.join(outgif,year) )
			if not os.path.isdir( os.path.join(outgif,year,month) ):
				os.mkdir( os.path.join(outgif,year,month) )
			if not os.path.isdir( os.path.join(outgif,year,month,day) ):
				os.mkdir( os.path.join(outgif,year,month,day) )

			savepath = os.path.join(outgif,year,month,day)

			current_obj = None
			images 		= []

			for fitsfile in filelist:
				obj = re.sub( '\W+','',pf.getheader(fitsfile,ext=1)['OBJECT'] )
				print(fitsfile,obj)
				if obj != 'auto_focus':
					if current_obj != obj:
						if len(images) > 1:
							mjd = re.sub('\.', '','{:.4f}'.format( pf.getheader(fitsfile,ext=1)['MJD-OBS'] ) )
							obst = Time( pf.getheader(fitsfile,ext=1)['MJD-OBS'], format='mjd' )
							#set_trace()
							imageio.mimsave(savepath+'/'+current_obj+'_'+str(mjd)+'_centering.gif', images, duration=0.3)
							guide = Guider(	target 		= current_obj,
											obs_date 	= obst.iso,
											image 		= os.path.join(year,month,day,current_obj+'_'+str(mjd)+'_centering.gif'),
											site 		= site.upper(), )

							guide.save()



						current_obj = obj
						fits_data = pf.getdata(fitsfile, ext=1)
						fits_data = fits_data[400:700,600:900]
						#info = np.iinfo(fits_data.dtype)
						fits_data = fits_data.astype(np.float64) / 20000.
						fits_data = 255 * fits_data # Now scale by 255
						img = fits_data.astype(np.uint8)
						images = [img]
					else:
						fits_data = pf.getdata(fitsfile, ext=1)
						fits_data = fits_data[400:700,600:900]
						#info = np.iinfo(fits_data.dtype)
						fits_data = fits_data.astype(np.float64) / 20000.
						fits_data = 255 * fits_data # Now scale by 255
						img = fits_data.astype(np.uint8)
						images.append( img )

			if current_obj is not None:

				mjd = re.sub('\.', '','{:.4f}'.format( pf.getheader(fitsfile,ext=1)['MJD-OBS'] ) )
				obst = Time( pf.getheader(fitsfile,ext=1)['MJD-OBS'], format='mjd' )

				imageio.mimsave(savepath+'/'+current_obj+'_'+str(mjd)+'_centering.gif', images, duration=0.3)
				guide = Guider(	target 		= current_obj,
								obs_date 	= obst.iso,
								image 		= os.path.join(year,month,day,current_obj+'_'+str(mjd)+'_centering.gif'),
								site 		= site.upper(), )
				guide.save()
