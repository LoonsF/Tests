from app.main import repo
from app.schemas import ProductoCreate, ProductoUpdate


def test_integration_repo_operations():
    producto_creado = repo.crear(ProductoCreate(nombre="Test Integration", precio=15.5))
    assert producto_creado is not None
    assert producto_creado["nombre"] == "Test Integration"

    producto_obtenido = repo.obtener(producto_creado["id"])
    assert producto_obtenido == producto_creado

    productos = repo.listar()
    assert len(productos) == 1
    assert productos[0]["id"] == producto_creado["id"]

    update_data = ProductoUpdate(nombre="Test Updated", precio=25.5)
    producto_actualizado = repo.actualizar(producto_creado["id"], update_data)
    assert producto_actualizado["nombre"] == "Test Updated"
    assert producto_actualizado["precio"] == 25.5

    fue_eliminado = repo.eliminar(producto_creado["id"])
    assert fue_eliminado is True
    assert len(repo.listar()) == 0
