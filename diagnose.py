"""
Script de diagnóstico para verificar imports y configuración
"""
import sys
import os

# Añadir el directorio app al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

print("=== Diagnóstico de Imports ===\n")

# Test 1: Verificar imports básicos
print("1. Verificando imports de librerías base...")
try:
    import fastapi
    print("   ✓ FastAPI OK")
    import sqlalchemy
    print("   ✓ SQLAlchemy OK")
    import pydantic
    print("   ✓ Pydantic OK")
    import jose
    print("   ✓ python-jose OK")
    import passlib
    print("   ✓ passlib OK")
    import celery
    print("   ✓ Celery OK")
    import pika
    print("   ✓ pika OK")
except ImportError as e:
    print(f"   ✗ ERROR: {e}")
    print("   → Instalar dependencias: pip install -r app/requirements.txt")
    sys.exit(1)

print("\n2. Verificando módulos del proyecto...")
try:
    import config
    print("   ✓ config.py OK")
    print(f"      Database URL: {config.settings.database_url}")
except Exception as e:
    print(f"   ✗ ERROR en config.py: {e}")
    sys.exit(1)

try:
    import database
    print("   ✓ database.py OK")
except Exception as e:
    print(f"   ✗ ERROR en database.py: {e}")
    sys.exit(1)

try:
    import models
    print("   ✓ models.py OK")
except Exception as e:
    print(f"   ✗ ERROR en models.py: {e}")
    sys.exit(1)

try:
    import schemas
    print("   ✓ schemas.py OK")
except Exception as e:
    print(f"   ✗ ERROR en schemas.py: {e}")
    sys.exit(1)

try:
    import auth_utils
    print("   ✓ auth_utils.py OK")
except Exception as e:
    print(f"   ✗ ERROR en auth_utils.py: {e}")
    sys.exit(1)

try:
    import deps
    print("   ✓ deps.py OK")
except Exception as e:
    print(f"   ✗ ERROR en deps.py: {e}")
    sys.exit(1)

try:
    import crud
    print("   ✓ crud.py OK")
except Exception as e:
    print(f"   ✗ ERROR en crud.py: {e}")
    sys.exit(1)

try:
    import tasks
    print("   ✓ tasks.py OK")
except Exception as e:
    print(f"   ✗ ERROR en tasks.py: {e}")
    sys.exit(1)

try:
    import messaging
    print("   ✓ messaging.py OK")
except Exception as e:
    print(f"   ✗ ERROR en messaging.py: {e}")
    sys.exit(1)

try:
    from routers import auth, users
    print("   ✓ routers/auth.py OK")
    print("   ✓ routers/users.py OK")
except Exception as e:
    print(f"   ✗ ERROR en routers: {e}")
    sys.exit(1)

print("\n3. Verificando main.py y creación de la app...")
try:
    import main
    print("   ✓ main.py OK")
    print(f"   App title: {main.app.title}")
    print(f"   App version: {main.app.version}")
except Exception as e:
    print(f"   ✗ ERROR en main.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Verificando rutas registradas...")
try:
    routes = []
    for route in main.app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append(f"{list(route.methods)[0] if route.methods else 'GET'} {route.path}")
    
    print(f"   Total de rutas: {len(routes)}")
    for route in sorted(routes):
        print(f"   - {route}")
except Exception as e:
    print(f"   ✗ ERROR listando rutas: {e}")

print("\n=== Diagnóstico Completo ===")
print("Si llegaste hasta aquí, el código se puede importar correctamente.")
print("\nPróximos pasos:")
print("1. Verifica que Docker Desktop esté corriendo")
print("2. Ejecuta: docker compose up --build")
print("3. Verifica logs: docker compose logs api")
print("4. Si el contenedor se reinicia, revisa: docker compose logs api --tail=100")
