from django import forms
from .models import Equipo, TrasladoEquipo

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