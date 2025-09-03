from supabase import create_client, Client
from config import Config
from datetime import datetime
import traceback

class Database:
    def __init__(self):  # Corregido: era _init pero debe ser _init_
        try:
            self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            print("✅ Cliente de Supabase inicializado")
            print(f"🔗 URL: {Config.SUPABASE_URL}")
        except Exception as e:
            print(f"❌ Error inicializando Supabase: {e}")
            print(f"📋 Traceback: {traceback.format_exc()}")

    def create_table(self):
        """
        Crea la tabla usuarios en Supabase.
        NOTA: Esto debe ejecutarse en el SQL Editor de Supabase, no desde Python
        """
        sql_query = """
                    CREATE TABLE IF NOT EXISTS usuarios (
                                                            id SERIAL PRIMARY KEY,
                                                            nombre VARCHAR(100) NOT NULL,
                        telefono VARCHAR(20) NOT NULL,
                        pais VARCHAR(50) NOT NULL,
                        fecha_registro TIMESTAMP DEFAULT NOW()
                        );
                    """
        print("📝 Para crear la tabla, ejecuta este SQL en tu Supabase:")
        print(sql_query)
        return sql_query

    def insert_user(self, nombre, telefono, pais):
        """Inserta un nuevo usuario en la base de datos"""
        try:
            print(f"🔄 Intentando insertar usuario: {nombre}, {telefono}, {pais}")

            result = self.supabase.table('usuarios').insert({
                'nombre': nombre,
                'telefono': telefono,
                'pais': pais
            }).execute()

            print(f"📋 Respuesta completa de Supabase: {result}")

            if result.data and len(result.data) > 0:
                user_id = result.data[0]['id']
                print(f"✅ Usuario insertado con ID: {user_id}")
                return user_id
            else:
                print("❌ Error: No se pudo insertar el usuario - respuesta vacía")
                print(f"📋 Data: {result.data}")
                return None
        except Exception as e:
            print(f"❌ Error al insertar usuario: {e}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            return None

    def get_all_users(self):
        """Obtiene todos los usuarios de la base de datos"""
        try:
            print("🔄 Obteniendo usuarios de la base de datos...")

            result = self.supabase.table('usuarios').select('*').order('fecha_registro', desc=True).execute()

            print(f"📋 Respuesta completa de get_all_users: {result}")

            if result.data:
                users = result.data
                print(f"✅ Se obtuvieron {len(users)} usuarios")
                print(f"📋 Usuarios obtenidos: {users}")

                # Convertir fechas de string a datetime
                for user in users:
                    if 'fecha_registro' in user and user['fecha_registro']:
                        user['fecha_registro'] = self._convert_datetime(user['fecha_registro'])

                return users
            else:
                print("⚠ No se obtuvieron usuarios - result.data está vacío")
                return []

        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            return []

    def _convert_datetime(self, date_string):
        """Convierte string de fecha ISO a objeto datetime"""
        try:
            if date_string and isinstance(date_string, str):
                # Limpiar la fecha ISO: 2025-09-03T13:58:21.305438+00:00
                clean_date = date_string.split('.')[0].replace('T', ' ')
                if '+' in clean_date:
                    clean_date = clean_date.split('+')[0]
                return datetime.strptime(clean_date, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"⚠ Error convirtiendo fecha {date_string}: {e}")
        return date_string  # Devolver como string si no se puede convertir

    def test_connection(self):
        """Prueba la conexión a Supabase"""
        try:
            print("🧪 Probando conexión a Supabase...")

            # Intentar obtener la estructura de la tabla
            result = self.supabase.table('usuarios').select('*').limit(1).execute()

            print(f"📋 Resultado del test: {result}")
            print("✅ Test de conexión a Supabase exitoso")
            return True
        except Exception as e:
            print(f"❌ Error en test de conexión: {e}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            return False

    def debug_table_info(self):
        """Debug: Obtener información de la tabla"""
        try:
            print("🔍 Obteniendo información de debug de la tabla...")

            # Intentar hacer una consulta simple
            result = self.supabase.table('usuarios').select('count').execute()
            print(f"📊 Count result: {result}")

            # Intentar obtener un usuario
            result = self.supabase.table('usuarios').select('*').limit(1).execute()
            print(f"📋 Sample user: {result}")

        except Exception as e:
            print(f"❌ Error en debug: {e}")
            print(f"📋 Traceback: {traceback.format_exc()}")