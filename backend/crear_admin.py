#!/usr/bin/env python3
"""
Script para crear un usuario administrador inicial en el sistema Gestor LIME
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestorlime.settings')
django.setup()

from api.models import Usuario
from datetime import date

def crear_admin_inicial():
    """Crea un usuario administrador inicial si no existe"""
    
    # Verificar si ya existe un administrador
    admin_exists = Usuario.objects.filter(rol='admin').exists()
    
    if admin_exists:
        print("❌ Ya existe al menos un usuario administrador en el sistema.")
        print("📋 Usuarios administradores existentes:")
        admins = Usuario.objects.filter(rol='admin')
        for admin in admins:
            status = "✅ Activo" if admin.activo else "❌ Inactivo"
            print(f"   - {admin.nombreusuario} ({admin.get_nombre_display()}) - {status}")
        return
    
    print("🔧 Creando usuario administrador inicial...")
    
    # Crear usuario administrador por defecto
    admin_user = Usuario.objects.create(
        nombreusuario='admin',
        nombre_completo='Administrador del Sistema',
        email='admin@lime.udea.edu.co',
        telefono='',
        cargo='Administrador del Sistema',
        departamento='Sistemas',
        rol='admin',
        activo=True,
        creado_por='Sistema'
    )
    
    # Establecer contraseña por defecto
    admin_user.set_password('admin123')
    admin_user.save()
    
    print("✅ Usuario administrador creado exitosamente!")
    print("📋 Detalles del usuario:")
    print(f"   Usuario: {admin_user.nombreusuario}")
    print(f"   Contraseña: admin123")
    print(f"   Nombre: {admin_user.nombre_completo}")
    print(f"   Email: {admin_user.email}")
    print(f"   Rol: {admin_user.get_rol_display()}")
    print("")
    print("⚠️  IMPORTANTE:")
    print("   1. Cambia la contraseña después del primer inicio de sesión")
    print("   2. Actualiza el email y demás información personal")
    print("   3. Crea usuarios adicionales según sea necesario")
    print("")
    print("🌐 Puedes iniciar sesión en: http://localhost:8000/")

if __name__ == '__main__':
    crear_admin_inicial()