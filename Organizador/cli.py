"""Una simple agenda de tareas en la terminal."""

import argparse
from . import repo, io_json
from .tarea import Tarea

Archivo = "tareas.json"

def main():

    tareas_guardadas = io_json.cargar_tareas(Archivo)
    repo.cargar_tareas(tareas_guardadas)

    Tarea.sincronizar_contador(repo.obtener_todas_tareas())

    parser = argparse.ArgumentParser(description="Una simple agenda de tareas en la terminal.")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles', required=True)

    # Comando 'add'
    p_add = subparsers.add_parser('add', help='Añadir una nueva tarea.')
    p_add.add_argument('titulo', type=str, help='Título de la tarea.')
    p_add.add_argument('--descripcion', '-d', type=str, default="", help='Descripción de la tarea.')
    p_add.add_argument('--prioridad', '-p', type=int, default=1, choices=range(1, 6), help='Prioridad (1-5).')
    p_add.add_argument('--fecha', '-f', type=str, help='Fecha límite (AAAA-MM-DD).')
    p_add.add_argument('--etiquetas', '-e', type=str, nargs='*', help='Etiquetas separadas por espacio.')

    # Comando 'ls'
    p_ls = subparsers.add_parser('ls', help='Listar todas las tareas.')
    p_ls.add_argument('--por', type=str, default='titulo', choices=['fecha', 'prioridad', 'titulo'], help='Criterio de ordenación.')

    # Comando 'find'
    p_find = subparsers.add_parser('find', help='Buscar tareas por texto.')
    p_find.add_argument('texto', type=str, help='Texto a buscar en título o descripción.')

    # Comando 'done'
    p_done = subparsers.add_parser('done', help='Marcar una tarea como completada.')
    p_done.add_argument('id', type=str, help='ID de la tarea a completar.')

    # Comando 'rm'
    p_rm = subparsers.add_parser('rm', help='Eliminar una tarea.')
    p_rm.add_argument('id', type=str, help='ID de la tarea a eliminar.')
    
    # Comando 'save'
    p_save = subparsers.add_parser('save', help='Guardar tareas en un archivo JSON.')
    p_save.add_argument('archivo', type=str, help='Nombre del archivo JSON.')

    # Comando 'load'
    p_load = subparsers.add_parser('load', help='Cargar tareas desde un archivo JSON.')
    p_load.add_argument('archivo', type=str, help='Nombre del archivo JSON.')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    modified = False

    if args.command == 'add':
        try:
            tarea = Tarea(
                titulo=args.titulo,
                descripcion=args.descripcion,
                prioridad=args.prioridad,
                fecha=args.fecha,
                etiquetas=args.etiquetas
            )
            repo.agregar_tarea(tarea)
            modified = True
        except ValueError as e:
            print(f"Error: {e}")
            
    elif args.command == 'ls':
        repo.listar_tareas(ordenar_por=args.por)
        
    elif args.command == 'find':
        repo.buscar_tareas(args.texto)
        
    elif args.command == 'done':
        repo.marcar_completada(args.id)
        modified = True
        
    elif args.command == 'rm':
        repo.eliminar_tarea(args.id)
        modified = True

    elif args.command == 'save':
        io_json.guardar_tareas(repo.obtener_todas_tareas(), args.archivo)
        
    elif args.command == 'load':
        tareas = io_json.cargar_tareas(args.archivo)
        repo.cargar_tareas(tareas)
        modified = True

    if modified:
        io_json.guardar_tareas(repo.obtener_todas_tareas(), Archivo)
