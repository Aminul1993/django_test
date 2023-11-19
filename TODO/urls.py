from django.contrib import admin
from django.urls import path
from TODO.views import *

urlpatterns = [
	path('', todo_list, name="todo_list"),
	path('add/', todo_details, name="todo_add"),
	path('details/<int:gid>', todo_details, name="todo_details"),
	path('edit/', todo_save, name="todo_edit"),
	path('delete/<int:gid>', todo_delete, name="todo_delete"),
]