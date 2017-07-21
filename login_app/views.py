from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user
from django.views.generic import View
from .forms import RegForm, ContactForm
import numpy
from stl import mesh
import os
from subprocess import run as run_cmd
#from django.http import HttpResponse, Http404,HttpResponseRedirect
#from django.core.mail import EmailMessage, BadHeaderError

def home(request):											#calls the home page
	return render(request, 'login_app/home.html')

def register(request):										# calls the registration form
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/login_app/login')
	else:
		form = RegForm()
		args = {'regform':form}
		return render(request, 'login_app/reg_form.html', args)

def process_stl():									# function where stl file is processed
	from .estimator import gcoder
	from .estimator import rounder

	your_mesh = mesh.Mesh.from_file('temp_files/user_upload.stl')
	vol, cog, inertia = your_mesh.get_mass_properties()
	#print("Volume = ", format(vol), "mm^3")
	volume = format(vol)
	fname = os.path.join('temp_files/', 'user_upload.gcode')
	# Gcode file analysis
	gcode = gcoder.GCode(open(fname, "rU"))
	# print gcode
	'''print ("Dimensions:")
	xdims = (gcode.xmin, gcode.xmax, gcode.width)
	print ("\tX: %0.02f - %0.02f (%0.02f)" % xdims)
	ydims = (gcode.ymin, gcode.ymax, gcode.depth)
	print ("\tY: %0.02f - %0.02f (%0.02f)" % ydims)
	zdims = (gcode.zmin, gcode.zmax, gcode.height)
	print ("\tZ: %0.02f - %0.02f (%0.02f)" % zdims)
	print ("Filament used: %0.02fmm" % gcode.filament_length)
	print ("Number of layers: %d" % gcode.layers_count)
	print ("Estimated duration: %s" % gcode.estimate_duration()[1])
	print ("Estimated duration Hours: %0.02f" % gcode.duration_hours)'''
	#round to 0.5
	dur_in_hours = rounder.round_to_5(gcode.duration_hours)
	if dur_in_hours == 0:
	    dur_in_hours = 0.5
	#Multiply per hour cost
	#cost = dur_in_hours*300
	print ("\n")

	"""print_dict = {
	    "price": str(cost),
        "width": gcode.width,
        "depth": gcode.depth,
        "height": gcode.height,
        "filament_length": "%0.02f" % gcode.filament_length,
        "print_time": "%0.02f" % dur_in_hours
    }
	print (print_dict)"""

	os.remove('temp_files/user_upload.stl')
	os.remove('temp_files/user_upload.gcode')
	return volume, dur_in_hours

def contact(request):				# takes stl file and form data from user passes through process_stl and returns output
	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid() and request.FILES['myfile']:
			subject = form.cleaned_data['subject']
			your_email = form.cleaned_data['your_email']
			body = form.cleaned_data['body']
			myfile = request.FILES['myfile']
			fs = FileSystemStorage()
			filename = fs.save('user_upload.stl', myfile)
			quality = form.cleaned_data['quality']
			quantity = form.cleaned_data['quantity']
			global layer_thickness
			if quality == 'Best':
				# Change the path after cd the absolute path for the Cura folder wherever it is
				# ( ...\Fracktal-PrintCostEstimator\Cura if downloaded from Github).
				run_cmd('cd C:\\Users\Rohan\Documents\codes\wapps\print_cost_estimator\Cura && CuraEngine -s layerThickness=100 -s infillSpeed=60 -o ../temp_files/user_upload.gcode ../temp_files/user_upload.stl && cd ../login_app', shell=True)
			elif quality == 'High':
				run_cmd('cd C:\\Users\Rohan\Documents\codes\wapps\print_cost_estimator\Cura && CuraEngine -s layerThickness=200 -s infillSpeed=80 -o ../temp_files/user_upload.gcode ../temp_files/user_upload.stl && cd ../login_app', shell=True)
			elif quality == 'Normal':
				run_cmd('cd C:\\Users\Rohan\Documents\codes\wapps\print_cost_estimator\Cura && CuraEngine -s layerThickness=300 -s infillSpeed=80 -o ../temp_files/user_upload.gcode ../temp_files/user_upload.stl && cd ../login_app', shell=True)
			material = form.cleaned_data['material']
			color = form.cleaned_data['color']
			stl_data = process_stl()
			if material == 'PLA':
				weight = 1.25*(float(stl_data[0])/1000.0)
				cost_per_gm = 15.0
			elif material == 'ABS':
				weight = 1.04*(float(stl_data[0])/1000.0)
				cost_per_gm = 20.0
			cost_per_hr = 250.0
			cost = quantity*(cost_per_hr*stl_data[1] + weight*cost_per_gm)
			total_cost = cost + 250.0
			global body_all
			body_all = "Your Email Address: " + your_email + "\nSubject: " + subject + "\n\nBody: " + body + "\n\nQuality: " + quality + "\nMaterial: " + material + "\nColor: " + color + "\nVolume: " + stl_data[0] + " mm^3" + "\nPrint time estimate(in hrs): " + str(stl_data[1]) + "\nQuantity: " + str(quantity) + "\nEstimated print cost(INR): " + str(int(cost)) + " + INR 250 setup fee "
			body_short = "Body: " + body + "\n\nQuality: " + quality + "\nMaterial: " + material + "\nColor: " + color + "\nVolume: " + stl_data[0] + " mm^3" + "\nPrint time estimate(in hrs): " + str(stl_data[1]) + "\nEstimated cost(INR): " + str(int(cost))
			"""try:
				email = EmailMessage(subject, body_short, your_email, ['example@email.com'])
				#email.attach(attachment.name, attachment.read(), attachment.content_type)
				email.send()

			except BadHeaderError:
				return HttpResponse('Invalid Header Found')"""
			return redirect('/login_app/contact_success')
	return render(request, 'login_app/contact_mail.html', {'contact_form':form})

def contact_success(request):										# calls success page and prints output there
	args = {'stl_data':body_all}
	return render(request, 'login_app/contact_success.html', args)
