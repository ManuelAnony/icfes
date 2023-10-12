from flask import Flask, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Instancia de conexión a la base de datos
con_bd = Conexion()

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        usuario = con_bd.usuarios.find_one({"email": email})
        
        if usuario and usuario["password"] == password:
            session['email'] = usuario['email']
            #return redirect(url_for('index'))
            if usuario.get("rol") == "Administrador":
                 #Usuario es un administrador, redirigir a la página de administrador
                 flash('Inicio de sesión exitoso como administrador', 'success')
                 return redirect(url_for('index'))
            elif usuario.get("rol") == "Desarrollador":
                    #Usuario no es administrador, redirigir a la página de proyectos
                    flash('Inicio de sesión exitoso como usuario', 'success')
                    return redirect(url_for('proyecto'))
        else:   
            flash('Credenciales inválidas. Por favor, verifica tu email y contraseña.', 'danger')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        admin = "Desarrollador"
       
        existe_usuario = con_bd.usuarios.find_one({"email": email})
        
        if existe_usuario:
            
            return "El usuario ya existe. Por favor, inicia sesión o utiliza otro correo electrónico."
        else:
            
            nuevo_usuario = {
                "email": email,
                "password": password, 
                "rol": admin
            }
            con_bd.usuarios.insert_one(nuevo_usuario) 
            return redirect(url_for('index'))  

    return render_template('registro.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la sesión
    session.pop('email', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

# Ruta para la página de inicio (requiere inicio de sesión)
@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    # Obtener proyectos en curso desde la base de datos
    proyectos = con_bd.proyectos.find()
    return render_template('index.html', proyectos=proyectos)

@app.route('/registrar_proyecto', methods=['POST'])
def registrar_proyecto():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtén los datos del formulario
        nombre_proyecto = request.form.get("nombre_proyecto")
        descripcion = request.form.get("descripcion")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_finalizacion = request.form.get("fecha_finalizacion")
        estado = request.form.get("estado")

        # Implementa la lógica para registrar un nuevo proyecto en la base de datos
        nuevo_proyecto = {
            "nombre": nombre_proyecto,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio,
            "fecha_finalizacion": fecha_finalizacion,
            "estado": estado,
            "equipo": []  # Inicialmente sin equipo asignado
        }
        con_bd.proyectos.insert_one(nuevo_proyecto)

        flash('Proyecto registrado con éxito', 'success')
        return redirect(url_for('index'))

# Tu función de ruta para asignar equipo
# Ruta para el formulario de asignar equipo
@app.route('/asignar_equipo/<proyecto_id>', methods=['GET', 'POST'])
def asignar_equipo(proyecto_id):
    if request.method == 'POST':
        nombre_equipo = request.form.get("nombre_equipo")
        cantidad_miembros = int(request.form.get("cantidad_miembros"))
        miembros = []

        for i in range(cantidad_miembros):
            miembro = request.form.get(f"miembros_{i}")
            miembros.append(miembro)

        # Obtén la lista de usuarios con el rol "Desarrollador"
        usuarios_cursor = con_bd.usuarios.find({"rol": "Desarrollador"})
        usuarios = list(usuarios_cursor)

        # Guarda la información en la base de datos (proyecto)
        proyecto = con_bd.proyectos.find_one({"_id": ObjectId(proyecto_id)})
        proyecto["nombre_equipo"] = nombre_equipo
        proyecto["miembros_equipo"] = miembros
        con_bd.proyectos.update_one({"_id": ObjectId(proyecto_id)}, {"$set": proyecto})

        flash('Equipo asignado con éxito', 'success')
        return redirect(url_for('index'))

    # Envia la lista de usuarios "Desarrollador" a la plantilla
    usuarios_cursor = con_bd.usuarios.find({"rol": "Desarrollador"})
    usuarios = list(usuarios_cursor)

    return render_template('asignar_equipo.html', proyecto_id=proyecto_id, usuarios=usuarios)



@app.route('/notificar_equipo/<proyecto_id>', methods=['GET', 'POST'])
def notificar_equipo(proyecto_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtén los datos del formulario
        equipo_id = request.form.get('equipo_id')
        mensaje = request.form.get('mensaje')

        # Realiza la lógica para notificar al equipo, por ejemplo, enviar correos o notificaciones

        flash(f'Notificación enviada al equipo {equipo_id} del proyecto {proyecto_id}', 'success')

    # Puedes obtener más información sobre el proyecto, como el equipo asignado, a través de la base de datos aquí
    # proyecto = con_bd.proyectos.find_one({"_id": proyecto_id})
    # equipo = con_bd.equipos.find({"proyecto_id": proyecto_id})

    return render_template('notificar_equipo.html', proyecto_id=proyecto_id)

@app.route('/asignar_equipo', methods=['GET'])
def mostrar_formulario_asignar_equipo():
    # Obtén la lista de usuarios con el rol "Desarrollador" desde tu base de datos
    usuarios_desarrolladores = con_bd.usuarios.find({"rol": "Desarrollador"})

    return render_template('asignar_equipo.html', usuarios=usuarios_desarrolladores)

@app.route('/proyecto')
def proyecto():
    if 'email' not in session:
        return redirect(url_for('login'))

    # Consulta para obtener los proyectos asignados al administrador
    proyectos_cursor = con_bd.proyectos.find({"miembros_equipo": session['email']})
    proyectos = list(proyectos_cursor)

    # Consulta para obtener las actividades relacionadas con cada proyecto
    actividades_por_proyecto = {}  # Un diccionario para almacenar actividades por proyecto

    for proyecto in proyectos:
        actividades_cursor = con_bd.actividades.find({"proyecto_id": proyecto['_id']})
        actividades = list(actividades_cursor)
        actividades_por_proyecto[proyecto['_id']] = actividades

    return render_template('proyecto.html', proyectos=proyectos, actividades_por_proyecto=actividades_por_proyecto)

@app.route('/crear_actividad', methods=['POST'])
def crear_actividad():
    if request.method == 'POST':
        # Procesa la información del formulario para crear una nueva actividad
        admin_email = request.form.get("admin_email")
        nombre_actividad = request.form.get("nombre_actividad")
        fecha_vencimiento = request.form.get("fecha_vencimiento")
        proyecto_id = ObjectId(request.form.get("proyecto_id"))

        # Aquí debes guardar la información en la base de datos, por ejemplo, en la colección de actividades
        nueva_actividad = {
            "admin_email": admin_email,
            "nombre": nombre_actividad,
            "fecha_vencimiento": fecha_vencimiento,
            "proyecto_id": proyecto_id
        }
        con_bd.actividades.insert_one(nueva_actividad)

        flash('Actividad creada con éxito', 'success')
        return redirect(url_for('proyecto'))

@app.route('/editar_estado/<proyecto_id>', methods=['GET', 'POST'])
def editar_estado(proyecto_id):
    if request.method == 'POST':
        nuevo_estado = request.form.get("nuevo_estado")

        # Actualiza el estado del proyecto en la base de datos
        proyecto = con_bd.proyectos.find_one({"_id": ObjectId(proyecto_id)})
        proyecto["estado"] = nuevo_estado
        con_bd.proyectos.update_one({"_id": ObjectId(proyecto_id)}, {"$set": proyecto})

        flash('Estado del proyecto actualizado', 'success')
        return redirect(url_for('proyecto'))

    # Obtén el proyecto que se va a editar y pasa su estado actual al formulario
    proyecto = con_bd.proyectos.find_one({"_id": ObjectId(proyecto_id)})
    estado_actual = proyecto.get("estado")

    return render_template('editar_estado.html', proyecto_id=proyecto_id, estado_actual=estado_actual)

@app.route('/eliminar_proyecto/<proyecto_id>')
def eliminar_proyecto(proyecto_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    # Agrega la lógica para eliminar el proyecto en función de su ID
    proyecto = con_bd.proyectos.find_one({"_id": ObjectId(proyecto_id)})

    if proyecto:
        con_bd.proyectos.delete_one({"_id": ObjectId(proyecto_id)})
        flash('Proyecto eliminado con éxito', 'success')
    else:
        flash('Proyecto no encontrado', 'danger')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
