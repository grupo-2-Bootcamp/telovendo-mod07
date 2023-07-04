from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from telovendo.models import CustomUser, Empresas, Estado_Pedido, Pedidos, Productos, Direcciones, MetodoPago, Detalles_Pedido
from django.contrib.auth.models import User, Group


# Formulario de creación de usuarios solo para el panel de administración de Django

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('run', 'group', 'idEmpresa', )

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = UserChangeForm.Meta.fields

# Otros formularios

# Formulario de login
class FormularioLogin(forms.Form):
    email = forms.EmailField        (label='Email', required=True,
                                        max_length=30,
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
    password = forms.CharField      (label='Contraseña', required=True,
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
    username = forms.CharField      (label='Nombre de usuario', required=True,
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
    first_name = forms.CharField    (label='Primer nombre', required = True,
                                        max_length=30,
                                        error_messages={
                                            'required': 'El primer nombre es obligatorio',
                                            'max_length': 'El primer nombre debe tener como maximo 30 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese su primer nombre',
                                            'class':'form-control'}),
                                    )
    last_name = forms.CharField     (label='Primer apellido', required = True,
                                        max_length=30,
                                        error_messages={
                                            'required': 'El primer apellido del usuario es obligatorio',
                                            'max_length': 'El primer apellido debe tener como maximo 30 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese su primer apellido',
                                            'class':'form-control'}),
                                    )
    email = forms.EmailField        (label='Dirección de email', required = True, 
                                        max_length=30,
                                        error_messages={
                                            'required': 'Tiene que indicar el email del usuario',
                                            'max_length': 'La dirección de email tiene más de 30 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                                'placeholder':'Ingrese su correo electrónico',
                                                'class':'form-control',
                                                'type':'email'})
                                    )
    run = forms.CharField           (label='RUN', required = True,
                                    max_length=12,
                                        error_messages={
                                            'required': 'El RUN del usuario es obligatorio',
                                            'max_length': 'El RUN no debe sobrepasar los 12 carácteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese su RUN',
                                            'class':'form-control'}),
                                    )
    idEmpresa = forms.ModelChoiceField(label='Empresa', empty_label=('Seleccione una empresa'),
                                        queryset=Empresas.objects.all(), required=False, 
                                        widget= forms.Select(attrs={
                                            'class':'form-select'}),)
    group = forms.ModelChoiceField(
                                    label='Grupo',
                                    queryset=Group.objects.filter(name='Clientes'),
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'form-select'}),
                                )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email', 'run', 'idEmpresa', 'group')

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


class FormularioUpdateEstado(forms.ModelForm):
    idEstado = forms.ModelChoiceField(label='Estado', empty_label=('Seleccione un estado'),
                                        queryset=Estado_Pedido.objects.all(), required=False, 
                                        widget= forms.Select(attrs={
                                            'class':'form-select'}),)
    class Meta:
        model = Pedidos
        fields = ('idEstado',)
        labels = {'idEstado': 'Nuevo estado a actualizar',}
        widgets = {
            'idEstado': forms.Select(attrs={'class': 'form-select', 'required': True,}, ),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idEstado'].empty_label = 'Seleccione un estado'

class FormularioProductos(forms.Form):
    nombre = forms.CharField    (label='Nombre del producto', required = True,
                                        max_length=45,
                                        error_messages={
                                            'required': 'El nombre del producto es obligatorio',
                                            'max_length': 'El nombre debe tener como maximo 45 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el nombre del producto',
                                            'class':'form-control'}),
                                    )

    descripcion =  forms.CharField    (label='Descripción', required = True,
                                        max_length=45,
                                        error_messages={
                                            'required': 'La descripción del producto es obligatoria',
                                            'max_length': 'La descripción debe tener como maximo 45 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese la descripcion del producto es obligatorio',
                                            'class':'form-control'}),
                                    )

    stock = forms.IntegerField      (label='Stock', required = True,
                                        error_messages={
                                            'required': 'El stock del producto es obligatorio',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el stock del producto',
                                            'class':'form-control'}),
                                    )

    precio = forms.IntegerField    (label='Precio', required = True,
                                        error_messages={
                                            'required': 'El precio del producto es obligatorio',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el precio del producto',
                                            'class':'form-control'}),
                                    )
    
class FormularioEditarProductos(forms.ModelForm):
    nombre = forms.CharField    (label='Nombre del producto', required = False,
                                        max_length=45,
                                        error_messages={
                                            'max_length': 'El nombre debe tener como maximo 45 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el nombre del producto',
                                            'class':'form-control'}),
                                    )

    descripcion =  forms.CharField    (label='Descripción', required = False,
                                        max_length=45,
                                        error_messages={
                                            'max_length': 'La descripción debe tener como maximo 45 caracteres',
                                        },
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese la descripcion del producto es obligatorio',
                                            'class':'form-control'}),
                                    )

    stock = forms.IntegerField      (label='Stock', required = False,
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el stock del producto',
                                            'class':'form-control'}),
                                    )

    precio = forms.IntegerField    (label='Precio', required = False,
                                        widget= forms.TextInput(attrs={
                                            'placeholder': 'Ingrese el precio del producto',
                                            'class':'form-control'}),
                                    )
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'stock', 'precio']

class FormularioPedidos(forms.ModelForm):

    idEmpresa = forms.ModelChoiceField      (label='Empresa', empty_label=('Seleccione una empresa'), queryset=Empresas.objects.all(), required=True,
                                            widget= forms.Select(attrs={
                                                'class':'form-select'}),
                                            )
    idDireccion = forms.ModelChoiceField    (label='Dirección', empty_label=('Seleccione una dirección'), queryset=Direcciones.objects.all(), required=True,
                                            widget= forms.Select(attrs={
                                                'class':'form-select'}),
                                            )
    instrucciones_entrega = forms.CharField  (label='Instrucciones de entrega', required = True,
                                            widget= forms.Textarea(attrs={
                                                'class':'form-control'}),
                                            )
    idMetodoPago = forms.ModelChoiceField    (label='Dirección', empty_label=('Seleccione un método de pago'), queryset=MetodoPago.objects.all(), required=True,
                                            widget= forms.Select(attrs={
                                                'class':'form-select'}),
                                            )
    
    class Meta:
        model = Pedidos
        fields = ['idEmpresa', 'idDireccion', 'instrucciones_entrega', 'idMetodoPago']

class FormularioDetalle(forms.ModelForm):

    idProductos = forms.ModelChoiceField    (label='Producto', empty_label=('Seleccione un producto'), queryset=Productos.objects.filter(stock__gt=0), required=True,
                                            widget= forms.Select(attrs={
                                                'class':'form-select'}),
                                            )
    cantidad = forms.IntegerField           (label='Cantidad de articulos', required = True,
                                             widget= forms.TextInput(attrs={
                                                'class':'form-control'}))

    class Meta:
        model = Detalles_Pedido
        fields = ['idProductos', 'cantidad']
