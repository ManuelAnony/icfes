# icfes

 Proyecto de Gestión de Proyectos
Este proyecto es una aplicación web desarrollada en Flask para la gestión de proyectos y tareas. Permite a los usuarios registrados, ya sean administradores o desarrolladores, crear proyectos, asignar equipos, y llevar un seguimiento del progreso de las tareas.

Funcionalidades
Registro e Inicio de Sesión: Los usuarios pueden registrarse en la plataforma proporcionando un correo electrónico y una contraseña. Pueden iniciar sesión con sus credenciales.

Roles de Usuario: Los usuarios pueden tener uno de dos roles: Administrador o Desarrollador. Los administradores tienen acceso a funciones adicionales.

Panel de Administrador: Los administradores pueden:

Ver una lista de proyectos en curso.
Asignar equipos de trabajo a proyectos.
Notificar a los miembros del equipo sobre su asignación.
Panel de Usuario (Desarrollador): Los desarrolladores pueden:

Ver los proyectos a los que han sido asignados.
Acceder a las tareas relacionadas con esos proyectos.
Actualizar el estado de las tareas.
Proyectos y Tareas: Cada proyecto tiene los siguientes detalles:

Nombre.
Descripción.
Fechas de inicio y finalización previstas.
Estado (pendiente, en proceso, completado).
Miembros del equipo asignados.
Equipos de trabajo (nombre y miembros).
Tareas relacionadas con el proyecto:
Nombre.
Descripción.
Fecha de vencimiento.
Estado (pendiente, en proceso, completado).
Interfaz de Usuario Amigable: La aplicación utiliza una interfaz de usuario fácil de usar con formularios y tablas para la gestión de proyectos y tareas.


Cómo Ejecutar la Aplicación
Requisitos Previos:

Asegúrate de tener Python y Flask instalados en tu sistema.
Clonar el Repositorio:

bash
Copy code
git clone https://github.com/tuusuario/proyecto-gestion.git
cd proyecto-gestion
Configuración:

Abre el archivo config.py y ajusta la configuración de la base de datos, como la URL de la base de datos MongoDB.
Crear un Entorno Virtual (Opcional):

bash
Copy code
python -m venv venv
source venv/bin/activate  # Para sistemas Unix
.\venv\Scripts\activate  # Para Windows
Instalar Dependencias:

Copy code
pip install -r requirements.txt
Ejecutar la Aplicación:

Copy code
python app.py
Acceder a la Aplicación:
Abre tu navegador web y visita http://localhost:5000.
