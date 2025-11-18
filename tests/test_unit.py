from app.repository import ProductoRepo
from app.schemas import ProductoCreate, ProductoUpdate
import pytest


def test_crear_producto_unit():
    repo = ProductoRepo()
    producto_data = ProductoCreate(nombre="Producto A", precio=10.5)

    producto = repo.crear(producto_data)

    assert producto["nombre"] == "Producto A"
    assert producto["precio"] == 10.5
    assert producto["id"] == 1
    assert len(repo.listar()) == 1


def test_obtener_producto_unit():
    repo = ProductoRepo()
    producto_data = ProductoCreate(nombre="Test", precio=15.0)
    producto_creado = repo.crear(producto_data)

    producto_obtenido = repo.obtener(producto_creado["id"])

    assert producto_obtenido == producto_creado


def test_obtener_producto_no_existente_unit():
    repo = ProductoRepo()
    producto = repo.obtener(999)

    assert producto is None


def test_actualizar_producto_unit():
    repo = ProductoRepo()
    producto_creado = repo.crear(ProductoCreate(nombre="Original", precio=10.0))

    update_data = ProductoUpdate(nombre="Actualizado", precio=20.0)
    producto_actualizado = repo.actualizar(producto_creado["id"], update_data)

    assert producto_actualizado["nombre"] == "Actualizado"
    assert producto_actualizado["precio"] == 20.0
    assert producto_actualizado["id"] == producto_creado["id"]


def test_eliminar_producto_unit():
    repo = ProductoRepo()
    producto_creado = repo.crear(ProductoCreate(nombre="Eliminar", precio=5.0))

    fue_eliminado = repo.eliminar(producto_creado["id"])

    assert fue_eliminado is True
    assert len(repo.listar()) == 0
    assert repo.obtener(producto_creado["id"]) is None
