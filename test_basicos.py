import pytest
import os
from Organizador.tarea import Tarea
from Organizador import repo, io_json

@pytest.fixture(scope="function")
def repositorio_limpio():
    repo._tareas = []
    archivo_test = 'test_tareas.json'

    yield archivo_test
    if os.path.exists(archivo_test):
        os.remove(archivo_test)

def test_agregar_y_verificar_tamano(repositorio_limpio):
    t1 = Tarea("Comprar leche", "Ir al supermercado")
    t2 = Tarea("Terminar juego", "Terminar el juego de Python")

    repo.agregar_tarea(t1)
    repo.agregar_tarea(t2)
    assert len(repo.obtener_todas_tareas()) == 2

def test_find_devuelve_tarea_esperada(repositorio_limpio):
    t1 = Tarea("Terminar Juego", "Pasar el silksong")
    repo.agregar_tarea(t1)
    resultado = repo.buscar_tareas("silksong")
    assert len(resultado) == 1
    assert resultado[0].titulo == "Terminar Juego"

def test_listar_por_fecha(repositorio_limpio):
    t1 = Tarea("Tarea del futuro", "", fecha="2025-12-01")
    t2 = Tarea("Tarea sin fecha", "")
    t3 = Tarea("Tarea mas reciente", "", fecha="2025-10-15")
    t4 = Tarea("Tarea del pasado", "", fecha="2020-01-01")
    repo.agregar_tarea(t1)
    repo.agregar_tarea(t2)
    repo.agregar_tarea(t3)
    repo.agregar_tarea(t4)

    tareas_ordenadas = repo.listar_tareas(ordenar_por='fecha')
    ids_esperados = [t4.id, t3.id, t1.id, t2.id]
    ids_obtenidos = [t.id for t in tareas_ordenadas]
    assert ids_obtenidos == ids_esperados

def test_completar_tarea(repositorio_limpio):
    t1 = Tarea("Tarea a completar", "")
    repo.agregar_tarea(t1)
    assert not t1.completada
    exito = repo.marcar_completada(t1.id)
    assert t1.completada
    assert exito is True

def test_cargar_tareas(repositorio_limpio):
    t1 = Tarea("Jugar", "Ir al entrenamiento")
    t2 = Tarea("Proyecto", "Corregir errores")
    repo.agregar_tarea(t1)
    repo.agregar_tarea(t2)

    archivo = "task.json"
    io_json.guardar_tareas(repo.obtener_todas_tareas(), "tareas.json")
    tareas_cargadas = io_json.cargar_tareas("tareas.json")
    repo.cargar_tareas(tareas_cargadas)
    assert len(repo.obtener_todas_tareas()) == 2
    assert repo.obtener_todas_tareas()[0].titulo == "Jugar"
    assert repo.obtener_todas_tareas()[1].titulo == "Proyecto"

    tareas_cargadas = io_json.cargar_tareas(archivo)
    repo.cargar_tareas(tareas_cargadas)
    assert len(repo.obtener_todas_tareas()) == 4
    assert repo.obtener_todas_tareas()[0].titulo == "Jugar Silksong"
    assert repo.obtener_todas_tareas()[1].titulo == "Entregar proyecto"
    assert repo.obtener_todas_tareas()[2].titulo == "Estudiar para lineal"
    assert repo.obtener_todas_tareas()[3].titulo == "Corregir bugs de codigo"

def test_eliminar_tarea(repositorio_limpio):
    t1 = Tarea("Tarea a eliminar", "")
    repo.agregar_tarea(t1)
    assert len(repo.obtener_todas_tareas()) == 1
    exito = repo.eliminar_tarea(t1.id)
    assert exito is True
    assert len(repo.obtener_todas_tareas()) == 0

def test_eliminar_tarea_inexistente(repositorio_limpio):
    t1 = Tarea("Tarea existente", "")
    repo.agregar_tarea(t1)
    exito = repo.eliminar_tarea("T-9999")
    assert exito is False
    assert len(repo.obtener_todas_tareas()) == 1

def test_marcar_completada_tarea_inexistente(repositorio_limpio):
    t1 = Tarea("Tarea existente", "")
    repo.agregar_tarea(t1)
    exito = repo.marcar_completada("T-9999")
    assert exito is False
    assert not t1.completada