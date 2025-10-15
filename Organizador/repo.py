"Clase que modela un repositorio en memoria de las tareas"

from .tarea import Tarea

_tareas = []

def agregar_tarea(tarea: Tarea):
    _tareas.append(tarea)
    print(f"Tarea '{tarea.titulo}' agregada con id {tarea.id}")

def listar_tareas(ordenar_por='titulo'):
    if not _tareas:
        print("No hay tareas para mostrar.")
        return []
    
    opciones_orden = {
        'fecha': lambda t: t.fecha or '9999-12-31',
        'prioridad': lambda t: t.prioridad,
        'titulo': lambda t: t.titulo.lower()
    }

    orden = opciones_orden.get(ordenar_por, opciones_orden['titulo'])
    tareas_ordenadas = sorted(_tareas, key=orden)
    for tarea in tareas_ordenadas:
        print(tarea)
    return tareas_ordenadas

def buscar_tareas(texto: str):
    resultados = [
        t for t in _tareas
        if texto.lower() in t.titulo.lower() or texto.lower() in t.descripcion.lower()
    ]
    if not resultados:
        print(f"No se encontraron tareas que contengan '{texto}'.")
    else:
        for tarea in resultados:
            print(tarea)
    return resultados

def marcar_completada(id_tarea: str):
    for tarea in _tareas:
        if tarea.id == id_tarea:
            tarea.completada = True
            print(f"Tarea '{tarea.titulo}' marcada como completada.")
            return True
    print(f"No se encontró tarea con id {id_tarea}.")
    return False

def eliminar_tarea(id_tarea: str):
    global _tareas
    len_inicial = len(_tareas)
    _tareas = [t for t in _tareas if t.id != id_tarea]
    if len(_tareas) < len_inicial:
        print(f"Tarea con id {id_tarea} eliminada.")
        return True
    print(f"No se encontró tarea con id {id_tarea}.")
    return False

def obtener_todas_tareas():
    return _tareas

def cargar_tareas(tareas):
    global _tareas
    _tareas = tareas
