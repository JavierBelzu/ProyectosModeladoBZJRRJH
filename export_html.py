# export_html.py

# Importamos la función para cargar tareas y la clase Tarea.
# Asumimos que io_json.py y tarea.py están en la misma carpeta.
from Organizador.io_json import cargar_tareas
from Organizador.tarea import Tarea

# Nombre del archivo de donde se leen los datos y a donde se escribe el HTML
ARCHIVO_JSON = "tareas.json"
ARCHIVO_HTML = "index.html"

def generar_html_tarea(tarea: Tarea) -> str:
    """Genera el bloque HTML para una única tarea."""
    # Se añade una clase 'completada' si la tarea lo está. [cite: 19]
    # Esto es clave para que el CSS pueda diferenciarla visualmente. [cite: 24]
    clase_completada = "completada" if tarea.completada else ""
    estado = "Completada" if tarea.completada else "Pendiente"

    # Estructura del elemento de la lista (<li>)
    return f"""
    <li class="tarea {clase_completada}">
        <div class="info">
            <span class="titulo">{tarea.titulo}</span>
            <span class="prioridad">(Prioridad: {tarea.prioridad})</span>
            <p class="descripcion">{tarea.descripcion or 'Sin descripción.'}</p>
        </div>
        <div class="estado">
            <span>{estado}</span>
            <span class="fecha">{tarea.fecha or 'Sin fecha'}</span>
        </div>
    </li>
    """

def exportar_tareas_a_html(tareas: list, archivo_salida: str):
    """Genera un archivo HTML a partir de una lista de tareas."""
    
    # 1. Separar tareas en pendientes y completadas [cite: 30]
    tareas_pendientes = sorted([t for t in tareas if not t.completada], key=lambda x: x.prioridad)
    tareas_completadas = sorted([t for t in tareas if t.completada], key=lambda x: x.prioridad)

    # 2. Generar el HTML para cada sección
    html_pendientes = "".join([generar_html_tarea(t) for t in tareas_pendientes])
    html_completadas = "".join([generar_html_tarea(t) for t in tareas_completadas])

    # 3. Manejar el caso de que no haya tareas [cite: 32]
    if not tareas:
        html_pendientes = "<li><p>¡Felicidades! No tienes tareas pendientes.</p></li>"

    # 4. Construir el documento HTML completo
    html_contenido = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Agenda de Tareas</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Mi Agenda de Tareas</h1>
    </header>
    <main>
        <section id="pendientes">
            <h2>Tareas Pendientes ({len(tareas_pendientes)})</h2> 
            <ul class="lista-tareas">
                {html_pendientes}
            </ul>
        </section>

        <section id="completadas">
            <h2>Tareas Completadas ({len(tareas_completadas)})</h2>
            <ul class="lista-tareas">
                {html_completadas}
            </ul>
        </section>
    </main>
</body>
</html>
"""

    # 5. Escribir el contenido en el archivo de salida
    try:
        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(html_contenido)
        print(f"✅ Reporte HTML generado exitosamente en '{archivo_salida}'")
    except IOError as e:
        print(f"❌ Error al escribir el archivo: {e}")


if __name__ == "__main__":
    # Obtener la lista de tareas desde el archivo JSON [cite: 17]
    lista_de_tareas = cargar_tareas(ARCHIVO_JSON)
    
    # Generar el archivo index.html [cite: 18]
    exportar_tareas_a_html(lista_de_tareas, ARCHIVO_HTML)