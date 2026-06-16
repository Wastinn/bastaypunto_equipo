from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_super_secreta_basta_y_punto'

# Puente de conexión a MySQL (XAMPP debe tener MySQL encendido)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="test"
    )

# ==========================================
# 1. VITRINA PÚBLICA (index)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Sacamos el mensaje de la sesión si existe, y lo borramos de la memoria inmediatamente (.pop)
    mensaje_exito = session.pop('mensaje_exito', '')
    
    # Lógica para recibir mensajes de contacto
    if request.method == 'POST' and 'enviar_mensaje' in request.form:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        if nombre and email and mensaje:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Mensajes_Contacto (Nombre, Email, Mensaje) VALUES (%s, %s, %s)",
                    (nombre, email, mensaje)
                )
                conn.commit()
                # Guardamos el mensaje en la sesión temporalmente en lugar de una variable
                session['mensaje_exito'] = f"¡Gracias, {nombre}! Tu mensaje fue guardado y te contactaremos pronto 🧵"
            except Exception as e:
                session['mensaje_exito'] = f"Hubo un error al guardar: {str(e)}"
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
            
            # ¡AQUÍ ESTÁ LA MAGIA! Redirigimos a la misma página para "limpiar" la petición POST
            return redirect(url_for('index'))

    # Traer servicios de la base de datos
    lista_servicios = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Servicios ORDER BY idServicio DESC")
        lista_servicios = cursor.fetchall()
    except Exception:
        pass
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    # TUS 6 ILUSTRACIONES SVG (Asegúrate de pegar tus 6 líneas largas aquí)
    dibujos_svg = [
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#fdf0c2"/><rect x="130" y="20" width="140" height="180" rx="8" fill="#d4b57e" opacity=".4"/><rect x="150" y="20" width="100" height="30" rx="4" fill="#c9a357"/><path d="M150 50 Q200 60 250 50 L265 200 Q200 210 135 200Z" fill="#c9a357" opacity=".85"/><rect x="168" y="52" width="64" height="4" rx="2" fill="#a07830"/><line x1="200" y1="58" x2="200" y2="195" stroke="#a07830" stroke-width="1.5" stroke-dasharray="4 4"/><rect x="130" y="80" width="22" height="60" rx="6" fill="#c9a357"/><rect x="248" y="80" width="22" height="60" rx="6" fill="#c9a357"/><rect x="180" y="135" width="40" height="5" rx="2" fill="#a07830"/><circle cx="200" cy="68" r="4" fill="#a07830"/><circle cx="200" cy="80" r="4" fill="#a07830"/></svg>',
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#d5ede4"/><path d="M140 40 Q200 30 260 40 L275 180 Q200 195 125 180Z" fill="#80c4a0" opacity=".7"/><path d="M163 40 Q200 35 237 40 L230 75 Q200 80 170 75Z" fill="#5dab80"/><circle cx="200" cy="115" r="12" fill="none" stroke="#3d8a60" stroke-width="1.5"/><circle cx="200" cy="115" r="5" fill="#3d8a60"/><line x1="200" y1="97" x2="200" y2="90" stroke="#3d8a60" stroke-width="1.5"/><line x1="215" y1="105" x2="221" y2="100" stroke="#3d8a60" stroke-width="1.5"/><line x1="215" y1="125" x2="221" y2="130" stroke="#3d8a60" stroke-width="1.5"/><line x1="185" y1="125" x2="179" y2="130" stroke="#3d8a60" stroke-width="1.5"/><line x1="185" y1="105" x2="179" y2="100" stroke="#3d8a60" stroke-width="1.5"/><circle cx="200" cy="88" r="5" fill="#80c4a0" stroke="#3d8a60" stroke-width="1"/><circle cx="223" cy="98" r="5" fill="#80c4a0" stroke="#3d8a60" stroke-width="1"/><circle cx="223" cy="132" r="5" fill="#80c4a0" stroke="#3d8a60" stroke-width="1"/><circle cx="177" cy="132" r="5" fill="#80c4a0" stroke="#3d8a60" stroke-width="1"/><circle cx="177" cy="98" r="5" fill="#80c4a0" stroke="#3d8a60" stroke-width="1"/><path d="M125 180 Q105 165 95 120 Q110 105 125 110Z" fill="#80c4a0" opacity=".8"/><path d="M275 180 Q295 165 305 120 Q290 105 275 110Z" fill="#80c4a0" opacity=".8"/></svg>',
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#e3daf5"/><path d="M155 40 L245 40 L270 200 L130 200Z" fill="#b09edd" opacity=".6"/><line x1="155" y1="40" x2="143" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="170" y1="40" x2="156" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="185" y1="40" x2="170" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="200" y1="40" x2="200" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="215" y1="40" x2="230" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="230" y1="40" x2="244" y2="200" stroke="#8b72c4" stroke-width="1.2"/><line x1="245" y1="40" x2="257" y2="200" stroke="#8b72c4" stroke-width="1.2"/><rect x="150" y="35" width="100" height="14" rx="4" fill="#7a5cb8"/><rect x="155" y="195" width="90" height="8" rx="4" fill="#7a5cb8" opacity=".6"/></svg>',
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#fde4d0"/><path d="M130 35 Q200 20 270 35 L285 200 Q200 215 115 200Z" fill="#d87050" opacity=".55"/><path d="M130 35 L155 35 L165 90 Q145 95 130 100Z" fill="#c05c3a"/><path d="M270 35 L245 35 L235 90 Q255 95 270 100Z" fill="#c05c3a"/><path d="M155 35 L200 50 L245 35 L240 95 Q200 105 160 95Z" fill="#c05c3a" opacity=".9"/><line x1="200" y1="50" x2="200" y2="200" stroke="#a04828" stroke-width="1.5" stroke-dasharray="3 3"/><rect x="172" y="110" width="14" height="14" rx="3" fill="#a04828"/><rect x="172" y="135" width="14" height="14" rx="3" fill="#a04828"/><rect x="172" y="160" width="14" height="14" rx="3" fill="#a04828"/><rect x="214" y="110" width="14" height="14" rx="3" fill="#a04828"/><rect x="214" y="135" width="14" height="14" rx="3" fill="#a04828"/><rect x="214" y="160" width="14" height="14" rx="3" fill="#a04828"/></svg>',
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#d6eaf5"/><path d="M155 25 L245 25 L250 115 Q220 125 200 120 Q180 125 150 115Z" fill="#5a8fbe" opacity=".6"/><path d="M150 115 Q165 120 185 115 L170 200 L130 200Z" fill="#4a80b0" opacity=".75"/><path d="M250 115 Q235 120 215 115 L230 200 L270 200Z" fill="#4a80b0" opacity=".75"/><line x1="200" y1="25" x2="200" y2="120" stroke="#2e6090" stroke-width="1.5"/><rect x="152" y="22" width="96" height="10" rx="4" fill="#2e6090"/><rect x="165" y="17" width="70" height="8" rx="4" fill="#5a8fbe"/><line x1="155" y1="25" x2="148" y2="115" stroke="#2e6090" stroke-width="1" stroke-dasharray="4 3" opacity=".7"/><line x1="245" y1="25" x2="252" y2="115" stroke="#2e6090" stroke-width="1" stroke-dasharray="4 3" opacity=".7"/></svg>',
        '<svg class="card-img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#fbeaf0"/><path d="M165 20 L235 20 L255 100 Q230 110 200 108 Q170 110 145 100Z" fill="#e87aa0" opacity=".65"/><path d="M145 100 Q170 112 200 110 Q230 112 255 100 L290 200 Q200 215 110 200Z" fill="#d4618a" opacity=".7"/><path d="M200 110 Q230 130 240 160" fill="none" stroke="#b04068" stroke-width="2"/><path d="M200 110 Q170 130 160 160" fill="none" stroke="#b04068" stroke-width="2"/><path d="M200 110 Q215 140 210 170" fill="none" stroke="#b04068" stroke-width="1.5"/><path d="M200 110 Q185 140 190 170" fill="none" stroke="#b04068" stroke-width="1.5"/><path d="M165 20 Q183 35 200 32 Q217 35 235 20" fill="none" stroke="#b04068" stroke-width="2"/><line x1="172" y1="20" x2="168" y2="0" stroke="#d4618a" stroke-width="3" stroke-linecap="round"/><line x1="228" y1="20" x2="232" y2="0" stroke="#d4618a" stroke-width="3" stroke-linecap="round"/></svg>'
    ]

    return render_template('index.html', lista_servicios=lista_servicios, dibujos_svg=dibujos_svg, mensaje_exito=mensaje_exito)

# ==========================================
# 2. SISTEMA DE LOGIN
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_admin, nombre, password FROM Administradores WHERE email = %s", (correo,))
            admin = cursor.fetchone()
            
            if admin and admin['password'] == contrasena:
                session['admin_id'] = admin['id_admin']
                session['admin_nombre'] = admin['nombre']
                return redirect(url_for('panel_admin'))
            else:
                flash('Credenciales incorrectas o correo no registrado.')
                
        except Exception as e:
            flash(f'Error en la validación: {str(e)}')
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    return render_template('login.html')

# ==========================================
# 3. PANEL DE ADMINISTRACIÓN
# ==========================================
@app.route('/panel_admin', methods=['GET', 'POST'])
def panel_admin():
    # Protección de ruta
    if 'admin_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Borrar Mensaje
        if 'borrar_mensaje' in request.form:
            id_borrar = request.form.get('id_mensaje')
            cursor.execute("DELETE FROM Mensajes_Contacto WHERE idMensaje = %s", (id_borrar,))
            conn.commit()
            
        # Borrar Servicio
        elif 'borrar_servicio' in request.form:
            id_srv = request.form.get('id_servicio')
            cursor.execute("DELETE FROM Servicios WHERE idServicio = %s", (id_srv,))
            conn.commit()
            
        # Agregar Servicio
        elif 'agregar_servicio' in request.form:
            nombre = request.form.get('name', '').strip()
            desc = request.form.get('descripcion', '').strip()
            precio = request.form.get('precio_base', '0').strip()
            tiempo = request.form.get('tiempo_estimado', '').strip()
            
            if nombre:
                cursor.execute(
                    "INSERT INTO Servicios (Name, Descripción, Precio_Base, Tiempo_Estimado) VALUES (%s, %s, %s, %s)",
                    (nombre, desc, precio, tiempo)
                )
                conn.commit()
                
        return redirect(url_for('panel_admin'))

    # Cargar datos para la vista
    cursor.execute("SELECT * FROM Mensajes_Contacto ORDER BY Fecha_Envio DESC")
    mensajes = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Servicios")
    servicios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('panel_admin.html', mensajes=mensajes, servicios=servicios)

# ==========================================
# 4. CERRAR SESIÓN
# ==========================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)