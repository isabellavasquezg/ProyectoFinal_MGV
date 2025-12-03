#!/usr/bin/env python3
"""
Script para verificar y corregir usuarios en el sistema Gestor LIME
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestorlime.settings')
django.setup()

from api.models import Usuario

def verificar_usuarios():
    """Verifica todos los usuarios en el sistema"""
    
    print("🔍 VERIFICANDO USUARIOS EN EL SISTEMA")
    print("=" * 50)
    
    usuarios = Usuario.objects.all()
    
    if not usuarios:
        print("❌ No se encontraron usuarios en el sistema.")
        return
    
    print(f"📊 Total de usuarios encontrados: {usuarios.count()}")
    print("")
    
    for usuario in usuarios:
        status = "✅ Activo" if usuario.activo else "❌ Inactivo"
        print(f"👤 Usuario: {usuario.nombreusuario}")
        print(f"   Nombre: {usuario.nombre_completo or 'No especificado'}")
        print(f"   Email: {usuario.email or 'No especificado'}")
        print(f"   Rol: {usuario.get_rol_display()}")
        print(f"   Estado: {status}")
        print(f"   Fecha creación: {usuario.fecha_creacion}")
        
        # Verificar contraseñas comunes
        contraseñas_test = ['admin123', 'admin', '12345', '123456', 'password']
        for pwd in contraseñas_test:
            if usuario.check_password(pwd):
                print(f"   🔑 Contraseña funcional: {pwd}")
                break
        else:
            print(f"   🔒 Contraseña: No coincide con las comunes probadas")
        
        print("-" * 30)

def reset_password_admin():
    """Resetea la contraseña del usuario admin"""
    
    try:
        admin_user = Usuario.objects.get(nombreusuario='admin')
        
        print("\n🔧 RESETEANDO CONTRASEÑA DEL ADMIN")
        print("=" * 40)
        
        # Establecer nueva contraseña
        nueva_password = 'admin123'
        admin_user.set_password(nueva_password)
        admin_user.save()
        
        print(f"✅ Contraseña del usuario 'admin' reseteada exitosamente!")
        print(f"🔑 Nueva contraseña: {nueva_password}")
        print(f"👤 Usuario: admin")
        print("")
        print("⚠️  Recuerda cambiar esta contraseña después del primer login.")
        
        # Verificar que funcione
        if admin_user.check_password(nueva_password):
            print("✅ Verificación exitosa: La nueva contraseña funciona correctamente.")
        else:
            print("❌ Error: La nueva contraseña no se guardó correctamente.")
            
    except Usuario.DoesNotExist:
        print("❌ No se encontró el usuario 'admin'.")
        print("💡 Ejecuta crear_admin.py para crear el usuario administrador.")

def crear_usuario_test():
    """Crea un usuario de prueba adicional"""
    
    print("\n🆕 CREANDO USUARIO DE PRUEBA")
    print("=" * 35)
    
    # Verificar si ya existe
    if Usuario.objects.filter(nombreusuario='test').exists():
        print("❌ Ya existe un usuario 'test'.")
        return
    
    test_user = Usuario.objects.create(
        nombreusuario='test',
        nombre_completo='Usuario de Prueba',
        email='test@lime.udea.edu.co',
        rol='editor',
        activo=True,
        creado_por='Sistema'
    )
    
    test_user.set_password('12345')
    test_user.save()
    
    print("✅ Usuario de prueba creado exitosamente!")
    print("👤 Usuario: test")
    print("🔑 Contraseña: 12345")
    print("🏷️  Rol: Editor")

def menu_principal():
    """Menú principal del script"""
    
    while True:
        print("\n🛠️  GESTOR DE USUARIOS - SISTEMA LIME")
        print("=" * 40)
        print("1. Verificar todos los usuarios")
        print("2. Resetear contraseña del admin")
        print("3. Crear usuario de prueba")
        print("4. Salir")
        print("")
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            verificar_usuarios()
        elif opcion == '2':
            reset_password_admin()
        elif opcion == '3':
            crear_usuario_test()
        elif opcion == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == '__main__':
    menu_principal()