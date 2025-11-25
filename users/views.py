from django.shortcuts import render
from .forms import UserForm
from .models import User

def home_page(request):
    return render(request, 'support/home.html')

def user_application(request):
    form = UserForm()
    if request.method == 'POST':
        User.objects.create(
            name=request.POST('name'),
            email=request.POST('email'),
            phone_number=request.POST('phone_number'),
            message=request.POST('message'),
        )
        context = {'form': form}
        return render(request, 'users/application.html', context)
    else:
        return render(request, 'support/user_application.html')
