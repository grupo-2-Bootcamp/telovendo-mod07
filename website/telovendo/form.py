from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from telovendo.models import CustomUser, Empresas
from django.contrib.auth.models import User, Group


# Formulario de creación de usuarios solo para el panel de administración de Django

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('run', 'group', 'idEmpresa', )

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        # fields = ('id', 'email', 'username', 'first_name', 'last_name', 'run', 'idEmpresa', 'group')
        fields = UserChangeForm.Meta.fields

# Otros formularios

# Formulario de login
class FormularioLogin(forms.Form):
        email = forms.EmailField(label="Email", required=True, max_length=30,
                                error_messages={
                                    'required': 'Tiene que indicar el email del usuario',
                                    'max_length': 'La dirección de email tiene más de 30 caracteres',
                                },
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Ingrese su correo electrónico',
                                    'class': 'form-control',
                                    'type': 'email'
                                })
                                )
        password = forms.CharField(label='Contraseña', required=True,
                                max_length=30, min_length=6,
                                error_messages={
                                    'required': 'La contraseña es obligatoria',
                                    'max_length': 'La contraseña no puede superar los 30 caracteres',
                                    'min_length': 'La contraseña debe tener al menos 8 caracteres'
                                },
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Ingrese su contraseña',
                                    'class': 'form-control'
                                })
                                )

class FormularioRegistro(forms.ModelForm):
    username = forms.CharField(label='NombreUsuario', required=True,
                                max_length=30, min_length=5,
                                error_messages={
                                    'required': 'El nombre de usuario es obligatorio',
                                    'max_length': 'El usuario no puede superar los 30 caracteres',
                                    'min_length': 'El usuario debe tener al menos 5 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Ingrese su nombre de usuario',
                                    'class': 'form-control'
                                })
                                )
    first_name = forms.CharField            (label="Nombre", required = True, max_length=30,
                                        error_messages={
                                            'required': 'El nombre del usuario es Obligatorio',
                                            'max_length': 'El nombre debe tener como maximo 30 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el nombre del usuario',
                                            'class':'form-control'}),
                                        )

    last_name = forms.CharField          (label="Apellido", required = True, max_length=30,
                                        error_messages={
                                            'required': 'El apellido del usuario es obligatorio',
                                            'max_length': 'El apellido debe tener como maximo 30 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el apellido del usuario',
                                            'class':'form-control'}),
                                        )
    email = forms.EmailField    (label="Email", required = True, max_length=30,
                                    error_messages={
                                            'required': 'Tiene que indicar el email del usuario',
                                            'max_length': 'La dirección de email tiene más de 30 caracteres',
                                        },
                                    widget= forms.TextInput(attrs={
                                            'placeholder':'Ingrese su correo electrónico',
                                            'class':'form-control',
                                            'type':'email'})
                                    )
    run = forms.CharField            (label="Run", required = True, max_length=12,
                                        error_messages={
                                            'required': 'El run del usuario es obligatorio',
                                            'max_length': 'El run no debe sobrepasar los 12 carácteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese su run',
                                            'class':'form-control'}),
                                        )                  
    # password1 = forms.CharField(label='Contraseña', required=True,
    #                             max_length=30, min_length=1,
    #                             error_messages={
    #                                 'required': 'La contraseña es obligatoria',
    #                                 'max_length': 'La contraseña no puede superar los 30 caracteres'
    #                                 },
    #                             widget=forms.PasswordInput(attrs={
    #                                 'placeholder': 'Ingrese su contraseña',
    #                                 'class': 'form-control'
    #                             })
    #                             )
    # password2 = forms.CharField(label='Contraseña', required=True,
    #                             max_length=30, min_length=1,
    #                             error_messages={
    #                                 'required': 'La contraseña es obligatoria',
    #                                 'max_length': 'La contraseña no puede superar los 30 caracteres'
    #                                 },
    #                             widget=forms.PasswordInput(attrs={
    #                                 'placeholder': 'Ingrese su contraseña',
    #                                 'class': 'form-control'
    #                             })
    #                             )
    empresas = forms.ModelChoiceField(queryset=Empresas.objects.all(), required=False)
    
    # group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email')