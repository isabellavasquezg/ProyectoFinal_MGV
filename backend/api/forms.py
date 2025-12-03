from django import forms
from .models import Equipo, TrasladoEquipo, Usuario

class EquipoForm(forms.ModelForm):
    """Formulario para crear y editar equipos"""
    
    class Meta:
        model = Equipo
        exclude = ['id']  # Excluir el ID ya que es auto-generado
        
        widgets = {
            # Información General
            'proceso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: LIME'}),
            'nombre_equipo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Nombre del equipo'}),
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código interno'}),
            'codigo_ips': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código IPS'}),
            'codigo_ecri': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código ECRI'}),
            
            # Responsabilidad y Ubicación
            'responsable': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Responsable del equipo'}),
            'ubicacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ubicación del equipo'}),
            'sede': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar sede'),
                ('Prado', 'Prado'),
                ('SIU', 'SIU'),
                ('San Vicente', 'San Vicente'),
            ]),
            
            # Especificaciones Técnicas
            'marca': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Marca del equipo'}),
            'modelo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Modelo del equipo'}),
            'serie': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Número de serie'}),
            
            # Clasificaciones
            'clasificacion_misional': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Clasificación misional'}),
            'clasificacion_ips': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('BIO', 'BIO'),
                ('IND', 'IND'),
            ]),
            'clasificacion_riesgo': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('Clase I', 'Clase I'),
                ('Clase IIa', 'Clase IIa'),
                ('Clase IIb', 'Clase IIb'),
                ('Clase III', 'Clase III'),
                ('NI', 'No Información'),
            ]),
            
            # Información Regulatoria
            'registro_invima': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Registro INVIMA'}),
            'tiempo_vida_util': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tiempo de vida útil'}),
            
            # Información de Compra
            'fecha_adquisicion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Fecha de adquisición'}),
            'propietario': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('UdeA', 'UdeA'),
                ('UT LIME', 'UT LIME'),
            ]),
            'fecha_fabricacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de fabricación'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT del proveedor'}),
            'proveedor': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Nombre del proveedor'}),
            'valor_compra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor de compra'}),
            
            # Garantía
            'en_garantia': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('Si', 'Si'),
                ('No', 'No'),
            ]),
            'fecha_fin_garantia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha fin garantía'}),
            
            # Documentos
            'forma_adquisicion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('Compra', 'Compra'),
                ('Donación', 'Donación'),
                ('Apoyo tecnológico', 'Apoyo tecnológico'),
            ]),
            'tipo_documento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tipo de documento'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            
            # Documentación Técnica
            'hoja_vida': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('SI', 'SI'),
                ('NO', 'NO'),
            ]),
            'registro_importacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Registro de importación'}),
            'manual_operacion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('SI', 'SI'),
                ('NO', 'NO'),
                ('NI', 'No Información'),
            ]),
            'manual_mantenimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Manual de mantenimiento'}),
            'guia_rapida': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('SI', 'SI'),
                ('NO', 'NO'),
                ('NI', 'No Información'),
            ]),
            'instructivo': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('SI', 'SI'),
                ('NO', 'NO'),
                ('NI', 'No Información'),
            ]),
            'protocolo_mto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Protocolo de mantenimiento'}),
            
            # Mantenimiento y Calibración
            'frecuencia_metrologica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frecuencia metrológica'}),
            'mantenimiento': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('Si', 'Si'),
                ('No', 'No'),
            ]),
            'frecuencia_mantenimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frecuencia mantenimiento'}),
            'calibracion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar'),
                ('Si', 'Si'),
                ('No', 'No'),
            ]),
            'frecuencia_calibracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frecuencia calibración'}),
            
            # Especificaciones Metrológicas
            'magnitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Magnitud'}),
            'rango': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Rango'}),
            'resolucion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Resolución'}),
            'rango_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Rango de trabajo'}),
            'error_maximo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Error máximo'}),
            
            # Especificaciones Eléctricas y Ambientales
            'voltaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Voltaje'}),
            'corriente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Corriente'}),
            'humedad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Humedad'}),
            'temperatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Temperatura'}),
            
            # Especificaciones Físicas
            'peso': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Peso'}),
            'dimensiones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dimensiones'}),
            'otros': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Otros datos'}),
            
            # Estado
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'proceso': 'Proceso',
            'nombre_equipo': 'Nombre del Equipo',
            'codigo_interno': 'Código Interno',
            'codigo_ips': 'Código IPS',
            'codigo_ecri': 'Código ECRI',
            'responsable': 'Responsable',
            'ubicacion': 'Ubicación',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'serie': 'Serie',
            'clasificacion_misional': 'Clasificación Misional',
            'clasificacion_ips': 'Clasificación IPS',
            'clasificacion_riesgo': 'Clasificación de Riesgo',
            'registro_invima': 'Registro INVIMA',
            'tiempo_vida_util': 'Tiempo de Vida Útil',
            'fecha_adquisicion': 'Fecha de Adquisición',
            'propietario': 'Propietario',
            'fecha_fabricacion': 'Fecha de Fabricación',
            'nit': 'NIT',
            'proveedor': 'Proveedor',
            'en_garantia': 'En Garantía',
            'fecha_fin_garantia': 'Fecha Fin Garantía',
            'forma_adquisicion': 'Forma de Adquisición',
            'tipo_documento': 'Tipo de Documento',
            'numero_documento': 'Número de Documento',
            'hoja_vida': 'Hoja de Vida',
            'registro_importacion': 'Registro de Importación',
            'manual_operacion': 'Manual de Operación',
            'manual_mantenimiento': 'Manual de Mantenimiento',
            'guia_rapida': 'Guía Rápida',
            'instructivo': 'Instructivo',
            'protocolo_mto': 'Protocolo de Mantenimiento',
            'frecuencia_metrologica': 'Frecuencia Metrológica',
            'mantenimiento': 'Mantenimiento',
            'frecuencia_mantenimiento': 'Frecuencia de Mantenimiento',
            'calibracion': 'Calibración',
            'frecuencia_calibracion': 'Frecuencia de Calibración',
            'magnitud': 'Magnitud',
            'rango': 'Rango',
            'resolucion': 'Resolución',
            'rango_trabajo': 'Rango de Trabajo',
            'error_maximo': 'Error Máximo',
            'voltaje': 'Voltaje',
            'corriente': 'Corriente',
            'humedad': 'Humedad',
            'temperatura': 'Temperatura',
            'peso': 'Peso',
            'otros': 'Otros',
            'sede': 'Sede',
            'activo': 'Activo',
            'dimensiones': 'Dimensiones',
            'valor_compra': 'Valor de Compra',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar equipo como activo por defecto
        self.fields['activo'].initial = True

class TrasladoForm(forms.ModelForm):
    class Meta:
        model = TrasladoEquipo
        fields = [
            'equipo',
            'sede_destino', 
            'ubicacion_destino',
            'responsable_destino',
            'justificacion',
            'observaciones'
        ]
        widgets = {
            'equipo': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'sede_destino': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=[
                ('', 'Seleccionar sede de destino'),
                ('Prado', 'Prado'),
                ('SIU', 'SIU'),
                ('San Vicente', 'San Vicente'),
            ]),
            'ubicacion_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación específica dentro de la sede',
                'required': True
            }),
            'responsable_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable en destino',
                'required': True
            }),
            'justificacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explique la razón del traslado',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
        labels = {
            'equipo': 'Equipo a trasladar',
            'sede_destino': 'Sede de destino',
            'ubicacion_destino': 'Ubicación de destino',
            'responsable_destino': 'Responsable en destino',
            'justificacion': 'Justificación del traslado',
            'observaciones': 'Observaciones'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo equipos activos
        self.fields['equipo'].queryset = Equipo.objects.filter(activo=True).order_by('nombre_equipo')
        
        # Personalizar el display del equipo
        self.fields['equipo'].empty_label = "Seleccione un equipo"
        
    def clean_sede_destino(self):
        sede = self.cleaned_data.get('sede_destino')
        if sede:
            sede = sede.strip()
            sedes_validas = ['Prado', 'San Vicente', 'SIU']
            if sede not in sedes_validas:
                raise forms.ValidationError(f'La sede debe ser una de: {", ".join(sedes_validas)}')
        return sede
        
    def clean_justificacion(self):
        justificacion = self.cleaned_data.get('justificacion')
        if justificacion and len(justificacion.strip()) < 10:
            raise forms.ValidationError('La justificación debe tener al menos 10 caracteres')
        return justificacion

class UsuarioForm(forms.ModelForm):
    """Formulario para crear y editar usuarios"""
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Dejar vacío para mantener la contraseña actual (solo en edición)'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = Usuario
        fields = [
            'nombreusuario', 'email', 'nombre_completo', 
            'telefono', 'cargo', 'departamento', 'rol', 'activo'
        ]
        widgets = {
            'nombreusuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuario único sin espacios'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del usuario'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo o posición'
            }),
            'departamento': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccionar departamento'),
                ('Administración', 'Administración'),
                ('Ingeniería Biomédica', 'Ingeniería Biomédica'),
                ('Mantenimiento', 'Mantenimiento'),
                ('Sistemas', 'Sistemas'),
                ('Calidad', 'Calidad'),
                ('Operaciones', 'Operaciones'),
            ]),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'nombreusuario': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'nombre_completo': 'Nombre Completo',
            'telefono': 'Teléfono',
            'cargo': 'Cargo',
            'departamento': 'Departamento',
            'rol': 'Rol del Usuario',
            'activo': 'Usuario Activo'
        }

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit:
            # En modo edición, hacer password opcional
            self.fields['password1'].help_text = 'Dejar vacío para mantener la contraseña actual'
            self.fields['password1'].required = False
            self.fields['password2'].required = False
        else:
            # En modo creación, password es obligatorio
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            self.fields['password1'].help_text = 'Mínimo 6 caracteres'

    def clean_nombreusuario(self):
        nombreusuario = self.cleaned_data.get('nombreusuario')
        if nombreusuario:
            nombreusuario = nombreusuario.strip().lower()
            # Validar que no tenga espacios
            if ' ' in nombreusuario:
                raise forms.ValidationError('El nombre de usuario no puede contener espacios')
            # Verificar unicidad (excluyendo instancia actual en edición)
            if self.instance.pk:
                if Usuario.objects.filter(nombreusuario=nombreusuario).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Este nombre de usuario ya existe')
            else:
                if Usuario.objects.filter(nombreusuario=nombreusuario).exists():
                    raise forms.ValidationError('Este nombre de usuario ya existe')
        return nombreusuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar unicidad del email (excluyendo instancia actual en edición)
            if self.instance.pk:
                if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Este correo electrónico ya está registrado')
            else:
                if Usuario.objects.filter(email=email).exists():
                    raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
            if len(password1) < 6:
                raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            usuario.set_password(password1)
        
        if commit:
            usuario.save()
        return usuario

class CambioPasswordForm(forms.Form):
    """Formulario específico para cambio de contraseña"""
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_nueva = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Mínimo 6 caracteres'
    )
    password_confirmacion = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, usuario, *args, **kwargs):
        self.usuario = usuario
        super().__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        password = self.cleaned_data.get('password_actual')
        if not self.usuario.check_password(password):
            raise forms.ValidationError('La contraseña actual es incorrecta')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password_nueva = cleaned_data.get('password_nueva')
        password_confirmacion = cleaned_data.get('password_confirmacion')
        
        if password_nueva and password_confirmacion:
            if password_nueva != password_confirmacion:
                raise forms.ValidationError('Las nuevas contraseñas no coinciden')
            if len(password_nueva) < 6:
                raise forms.ValidationError('La nueva contraseña debe tener al menos 6 caracteres')
        
        return cleaned_data