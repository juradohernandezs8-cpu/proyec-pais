from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import Database
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Inicializar la base de datos
db = Database()

@app.route('/')
def index():
    """Página principal con el formulario y la tabla de usuarios"""
    usuarios = db.get_all_users()
    return render_template('index.html', usuarios=usuarios)

@app.route('/registro', methods=['POST'])
def registro():
    """Procesa el registro de un nuevo usuario"""
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        pais = request.form.get('pais')

        # Validar que los campos no estén vacíos
        if not nombre or not telefono or not pais:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('index'))

        # Insertar usuario en la base de datos
        user_id = db.insert_user(nombre, telefono, pais)

        if user_id:
            flash(f'¡Bienvenido al Registro de Usuarios de Diferentes Países, {nombre}!', 'success')
        else:
            flash('Error al registrar el usuario. Intenta de nuevo.', 'error')

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/api/usuarios')
def api_usuarios():
    """API para obtener todos los usuarios en formato JSON"""
    usuarios = db.get_all_users()
    return jsonify(usuarios)

@app.route('/test')
def test_connection():
    """Ruta para probar la conexión a la base de datos"""
    if db.test_connection():
        return "✅ Conexión a Supabase exitosa!"
    else:
        return "❌ Error de conexión a Supabase"

if __name__ == '__main__':
    print("🚀 Iniciando aplicación Flask...")
    print("📊 Probando conexión a Supabase...")

    # Test de conexión al iniciar
    db.test_connection()

    # Mostrar SQL para crear tabla
    print("\n" + "="*50)
    print("📝 IMPORTANTE: Ejecuta este SQL en tu Supabase:")
    print("="*50)
    print(db.create_table())
    print("="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)