from django.shortcuts import render,redirect
from django.contrib import messages
import json
import requests
from .helper import *
from .forms import TODO

# Create your views here.

def todo_list(req):
	endpoint = ASANA_TASK_URL
	data = { "project": PROJECT_ID }
	resp = requests.get(endpoint, params=data, headers=HEADERS).json()
	return render(req, 'todo_list.html', resp)

def todo_details(req,gid=""):
	resp = {}
	custom_value = {}
	if gid != "":
		endpoint = ASANA_TASK_URL+"/"+str(gid)
		resp = requests.get(endpoint, headers=HEADERS).json()
		if 'data' in resp:
			if 'custom_fields' in resp['data']:
				for temp in resp['data']['custom_fields']:
					if temp['enum_value'] != None:
						custom_value[temp['gid']] = temp['enum_value']['gid']
	if not 'data' in resp:
		resp['data'] = {}
	resp['data']['custom_field'] = {}
	endpoint1 = ASANA_CUSTOM_URL
	resp1 = requests.get(endpoint1, headers=HEADERS).json()
	if 'data' in resp1:
		for temp in resp1['data']:
			if temp['custom_field']['enum_options'] != None:
				resp['data']['custom_field'][temp['custom_field']['gid']] = { "name": temp['custom_field']['name'], "options": {} }
				if temp['custom_field']['gid'] in custom_value:
					resp['data']['custom_field'][temp['custom_field']['gid']]['value'] = custom_value[temp['custom_field']['gid']]
				for temp1 in temp['custom_field']['enum_options']:
					resp['data']['custom_field'][temp['custom_field']['gid']]['options'][temp1['gid']] = temp1['name']
	return render(req, 'todo_details.html', resp)

def todo_save(req,gid=""):
	error_message = ""
	add = 1
	if req.method == "POST":
		form = TODO(req.POST)
		if form.is_valid():
			gid = form.cleaned_data["gid"]
			add = 1 if gid=="" else 0
			resp = {}
			endpoint = ASANA_TASK_URL+"/"+str(gid)
			HEADERS["content-type"] = "application/json"
			data = {
				"data": {
					"completed": form.cleaned_data["completed"],
					"name": form.cleaned_data["name"],
					"notes": form.cleaned_data["notes"],
					"custom_fields": {},
				}
			}
			for custom_fields in req.POST.getlist("custom_fields"):
				temp = custom_fields.split(':')
				data['data']['custom_fields'][temp[0]] = temp[1]
			if add == 0:
				resp = requests.put(endpoint, data=json.dumps(data), headers=HEADERS).json()
			else:
				data['data']['projects'] = [PROJECT_ID]
				resp = requests.post(endpoint, data=json.dumps(data), headers=HEADERS).json()
			if 'data' in resp:
				messages.success(req,'Saved Successfully')
				return redirect('todo_details',str(resp['data']['gid']))
			else:
				error_message = 'Server Error'
		else:
			error_message = 'Invalid Form'
	else:
		error_message = 'Invalid Method'
	messages.error(req,error_message)
	if add == 1:
		return redirect('todo_add')
	else:
		return redirect('todo_details',str(gid))

def todo_delete(req,gid):
	endpoint = ASANA_TASK_URL+"/"+str(gid)
	resp = requests.delete(endpoint, headers=HEADERS).json()
	messages.success(req,'Deleted Successfully')
	return redirect('todo_list')