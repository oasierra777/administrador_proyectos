from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic.edit import UpdateView

from .forms import LoginUserForm
from .forms import CreateUserForm
from .forms import EditUserForm
from .forms import EditUserPasswordForm
from .forms import EditClientForm
from .forms import EditClientSocial
from .models import Client
from .models import SocialNetwork

import json

"""
FUNCIONES
"""
@login_required(login_url = 'client:login')
def edit_password(request):
    form = EditUserPasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #obtengo la contrasena actual
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            if authenticate(username = request.user.username, password = current_password):
                request.user.set_password(new_password)
                request.user.save()
                #si queremos que permanesca con la sesion activa imporatr el metodo
                update_session_auth_hash(request, request.user)
                messages.success(request, 'password actualizado, messages')
            else:
                messages.error(request, 'No es posible actualizar el password, message')

    context = {'form': form}
    return render(request, 'client/edit_password.html', context)

@login_required(login_url = 'client:login')
def logout(request):
    logout_django(request)
    return redirect('client:login')

@login_required(login_url = 'client:login')
def edit(request):
    form_client = EditClientForm(request.POST or None, instance = client_instance(request.user))
    form_user = EditUserForm(request.POST or None, instance = request.user)
    if request.method == 'POST':
        if form_client.is_valid() and form_user.is_valid():
            form_user.save()
            form_client.save()
            messages.success(request, 'Datos actializados correctamente')
    context = {
        'form_client' : form_client,
        'form_user' : form_user
    }
    return render(request, 'client/edit.html', context)

def client_instance(user):
    try:
        return user.client
    except:
        return Client(user = user)

def user_filter(request):
    username = request.GET.get('username', '')#leemos todos los parametros que vengan del query
    users = User.objects.filter(username__startswith=username)
    users = [user_serialier(user) for user in users]
    return HttpResponse( json.dumps(users), content_type='application/json')

def user_serialier(user):
    return {'id' : user.id, 'username' : user.username}

"""
CLASES
"""
class ShowView(DetailView):
    model = User
    template_name = 'client/show.html'
    slug_field = 'username' #que campo de la base de datos
    slug_url_kwarg = 'username_url' #Es el de la url

class LoginView(View):
    form = LoginUserForm()
    message = None
    template = 'client/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('client:dashboard')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username_post = request.POST['username']
        password_post = request.POST['password']
        user = authenticate(username = username_post, password = password_post)
        if user is not None:
            login_django(request, user)
            return redirect('client:dashboard')
        else:
            self.message = 'username o password incorrectos'
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}

class DashboardView(LoginRequiredMixin, View):
    login_url = 'client:login' #este es sino esta autenticado se redirija alogin

    def get(self, request, *args, **kwargs):
        return render(request, 'client/dashboard.html', {})

class CreateView(CreateView):
    success_url = reverse_lazy('client:login')
    template_name = 'client/create.html'
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class EditSocialClass(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = 'client:login'
    model = SocialNetwork
    template_name = 'client/edit_social.html'
    success_url = reverse_lazy('client:edit_social')
    form_class = EditClientSocial
    success_message = 'Tu usuario ha sido actualizado exitosamente'

    def get_object(self, queryset = None):
        return self.get_social_instance()

    def get_social_instance(self):
        try:
            return self.request.user.SocialNetwork
        except:
            return SocialNetwork(user = self.request.user)
