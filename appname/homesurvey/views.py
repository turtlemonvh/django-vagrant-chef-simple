from django.contrib.auth import logout
from django.shortcuts import redirect, render, render_to_response

"""
Main project views
"""

def logoff(request):
    logout(request)
    return redirect('home')