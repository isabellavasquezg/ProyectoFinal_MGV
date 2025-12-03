#!/usr/bin/env python
"""
Script para verificar las tablas existentes en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestorlime.settings')
django.setup()

from django.db import connection

def check_tables():
    """Verificar qué tablas existen en la base de datos"""
    with connection.cursor() as cursor:
        # Mostrar todas las tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("Tablas existentes en la base de datos:")
        print("-" * 40)
        for table in tables:
            print(f"  - {table[0]}")
        
        print(f"\nTotal de tablas: {len(tables)}")
        
        # Verificar específicamente la tabla de traslados
        table_name = 'api_trasladoequipo'
        if any(table_name in table for table in tables):
            print(f"\n✓ La tabla '{table_name}' SÍ existe")
            
            # Mostrar estructura de la tabla
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print(f"\nEstructura de la tabla '{table_name}':")
            print("-" * 50)
            for column in columns:
                print(f"  {column[0]} - {column[1]} - {column[2]}")
        else:
            print(f"\n✗ La tabla '{table_name}' NO existe")
            
            # Mostrar tablas relacionadas con 'api'
            api_tables = [table[0] for table in tables if 'api_' in table[0]]
            print(f"\nTablas de la app 'api' encontradas:")
            for table in api_tables:
                print(f"  - {table}")

if __name__ == '__main__':
    check_tables()