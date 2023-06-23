from django import forms

class FormularioLogin(forms.Form):
    username = forms.CharField(label='Usuario', required=True,
                                max_length=30, min_length=5,
                                error_messages={
                                    'required': 'El usuario es obligatorio',
                                    'max_length': 'El nombre de usuario no puede ser superior a los 30 caracteres',
                                    'min_length': 'El nombre de usuario debe tener al menos 5 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Por favor, ingrese su nombre de usuario',
                                    'class': 'form-control'
                                })
                                )
    password = forms.CharField(label='Contraseña', required=True,
                                max_length=30, min_length=1,
                                error_messages={
                                    'required': 'La contraseña es obligatoria',
                                    'max_length': 'La contraseña no puede superar los 30 caracteres',
                                    'min_length': 'La contraseña debe tener al menos 1 caracter'
                                },
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Por favor, ingrese su contraseña',
                                    'class': 'form-control'
                                })
                                )