from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context["errors"] = form.errors
    form = UserCreationForm()
    context["form"] = form
    return render(request,"inscription.html",context=context)