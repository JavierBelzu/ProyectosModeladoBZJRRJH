"Clase que maneja la persistencia de tareas en formato JSON"

import json
from .tarea import Tarea

def guardar_tareas(tareas: list, archivo: str):
    lista_dict = [t.to_dict() for t in tareas]
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_dict, f, indent=4)
        print(f"Tareas guardadas exitosamente en '{archivo}'.")
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")

def cargar_tareas(archivo: str):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lista_dict = json.load(f)
        
        tareas_cargadas = []
        for d in lista_dict:
            tarea = Tarea(
                titulo=d['titulo'],
                descripcion=d['descripcion'],
                prioridad=d['prioridad'],
                fecha=d.get('fecha'),
                etiquetas=d.get('etiquetas')
            )
            tarea.id = d['id']
            tarea.completada = d['completada']
            tareas_cargadas.append(tarea)
            
        """ print(f"Tareas cargadas exitosamente desde '{archivo}'.") """
        return tareas_cargadas
    except FileNotFoundError:
        print(f"Advertencia: El archivo '{archivo}' no fue encontrado. Se inicia con una lista vacía.")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al leer el archivo JSON: {e}")
        return []