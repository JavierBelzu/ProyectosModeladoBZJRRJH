"""Clase que modela una Tarea"""

import datetime

class Tarea:
    contador_id = 1
    def __init__(self, titulo, descripcion, prioridad=1, fecha=None, etiquetas=None):
        
        self.id = f"T-{Tarea.contador_id:04d}"
        Tarea.contador_id += 1

        self.titulo = titulo
        self.descripcion = descripcion

        if not (1 <= prioridad <= 5):
            raise ValueError("La prioridad debe estar entre 1 y 5")
        self.prioridad = prioridad

        if fecha:
            try:
                datetime.datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                raise ValueError("La fecha debe estar en formato AAAA-MM-DD")
        self.fecha = fecha

        self.etiquetas = etiquetas if etiquetas is not None else []
        self.completada = False

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        return (f"[{estado}] {self.id}: {self.titulo} (P{self.prioridad}) " f"- Fecha: {self.fecha or 'N/A'}")
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "fecha": self.fecha,
            "etiquetas": self.etiquetas,
            "completada": self.completada
        }
    
    @staticmethod
    def sincronizar_contador(tareas):
        if not tareas:
            Tarea.contador_id = 1
            return
        
        max_id = 0
        for tarea in tareas:
            try:
                num_id = int(tarea.id.split('-')[1])
                if num_id > max_id:
                    max_id = num_id
            except (IndexError, ValueError):
                continue
        Tarea.contador_id = max_id + 1