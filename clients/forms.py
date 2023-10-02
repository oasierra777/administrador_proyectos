from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from clients.models import SocialNetwork

'''
CONSTANTS
'''
ERROR_MESSAGE_USER = {'required': 'El username es requerido', 'unique': 'El username se encuentra registrado',
                'invalid': 'El username es incorrecto'}
ERROR_MESSAGE_PASSWORD = {'required': 'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required': 'El email es requerido', 'invalid': 'Ingrese un email valido'}

'''
Funciones
'''
def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError('El password debe ser mayor a 5 carracteres desde la funcion')

'''
CLASES
'''

class LoginUserForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput(), validators = [must_be_gt])

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username_login', 'class': 'input_login'})
        self.fields['password'].widget.attrs.update({'id': 'password_login', 'class': 'input_login'})

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length = 20, error_messages = ERROR_MESSAGE_USER)
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput(),
        error_messages = ERROR_MESSAGE_PASSWORD, validators = [must_be_gt])
    email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username_create'})
        self.fields['password'].widget.attrs.update({'id': 'password_create'})
        self.fields['email'].widget.attrs.update({'id': 'email_create'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (User.objects.filter(email = email).count()):
            raise forms.ValidationError('El email debe ser unico, este ya esta creado')
        return email

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length = 20, error_messages = ERROR_MESSAGE_USER)
    email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (User.objects.filter(email = email).exclude(pk=self.instance.id).count()):
            raise forms.ValidationError('El email debe ser unico, este ya esta creado')
        return email

    class Meta:
        model = User
        fields = ('username', 'email')

class EditUserPasswordForm(forms.Form):
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput())
    new_password = forms.CharField(max_length = 20, widget = forms.PasswordInput(), validators = [must_be_gt])
    repeat_password = forms.CharField(max_length = 20, widget = forms.PasswordInput(), validators = [must_be_gt])

    def clean(self):
        clean_data = super(EditUserPasswordForm,self).clean()
        password1 = clean_data.get('new_password')
        password2 = clean_data.get('repeat_password')

        if password1 != password2:
            raise forms.ValidationError('Los password no son los mismos')

class EditClientForm(forms.ModelForm):

    job = forms.CharField(label = 'Trabajo Actual', required = False)
    bio = forms.CharField(label = 'Biografia', widget = forms.Textarea, required = False)
    class Meta:
        model = Client
        #fields = ('bio', 'job') solo nos interesa trabajar con estos dos campos
        exclude = ['user']

class EditClientSocial(forms.ModelForm):
    class Meta:
        model = SocialNetwork
        exclude = ['user']
