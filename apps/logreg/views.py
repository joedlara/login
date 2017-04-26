from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

def index(request):
	return render(request, 'logreg/index.html')


def register(request):
	context = {
	'fnom': request.POST['first_name'],
	'lnom': request.POST['last_name'],
	'e_address': request.POST['email'],
	'pass_word': request.POST['password'],
	'confirm_pass_word': request.POST['confirm'],
	'dob': request.POST['birthdate']
	}
	reg_results = User.objects.reg(context)
	
	if reg_results['new'] != None:
		#created new user
		#reg_results['new'] == new_user
		request.session['user_id'] = reg_results['new'].id
		request.session['user_fname'] = reg_results['new'].f_name
		return redirect('/success')

	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def success(request):
	if 'user_id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
		return redirect('/')
	return render(request, 'logreg/success.html')

def login(request):
	p_data = {
		'e_mail': request.POST['email'],
		'p_word': request.POST['password'],
	}

	log_results = User.objects.log(p_data)

	if log_results['list_errors'] != None:
		#get errors
		for error in log_results['list_errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect('/')

	else: 
		request.session['user_id'] = log_results['logged_user'].id
		request.session['user_fname'] = log_results['logged_user'].f_name
		return redirect('/success')

def logout(request):
	request.session.clear()
	return redirect('/')









