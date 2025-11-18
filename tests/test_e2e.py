import time
import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_e2e_ciclo_completo_producto():
    client = TestClient(app)
    timestamp = int(time.time())
    nombre_producto = f"Producto E2E {timestamp}"
    
    response_inicial = client.get("/productos")
    assert response_inicial.status_code == 200
    productos_iniciales = response_inicial.json()
    initial_count = len(productos_iniciales)
    
    data_crear = {"nombre": nombre_producto, "precio": 99.99}
    response_crear = client.post("/productos", json=data_crear)
    assert response_crear.status_code == 201
    producto_creado = response_crear.json()
    
    assert producto_creado["nombre"] == nombre_producto
    assert producto_creado["precio"] == 99.99
    producto_id = producto_creado["id"]
    
    response_despues_crear = client.get("/productos")
    assert response_despues_crear.status_code == 200
    assert len(response_despues_crear.json()) == initial_count + 1
    
    response_obtener = client.get(f"/productos/{producto_id}")
    assert response_obtener.status_code == 200
    producto_obtenido = response_obtener.json()
    assert producto_obtenido["id"] == producto_id
    
    data_actualizar = {"nombre": f"{nombre_producto} Actualizado", "precio": 149.99}
    response_actualizar = client.put(f"/productos/{producto_id}", json=data_actualizar)
    assert response_actualizar.status_code == 200
    producto_actualizado = response_actualizar.json()
    assert producto_actualizado["nombre"] == data_actualizar["nombre"]
    assert producto_actualizado["precio"] == data_actualizar["precio"]
    
    response_eliminar = client.delete(f"/productos/{producto_id}")
    assert response_eliminar.status_code == 200
    resultado_eliminar = response_eliminar.json()
    assert resultado_eliminar["status"] == "ok"
    assert resultado_eliminar["id_eliminado"] == producto_id
    
    response_obtener_despues = client.get(f"/productos/{producto_id}")
    assert response_obtener_despues.status_code == 404
    
    response_final = client.get("/productos")
    assert response_final.status_code == 200
    assert len(response_final.json()) == initial_count

def test_e2e_producto_no_existente():
    client = TestClient(app)
    response = client.get("/productos/9999")
    assert response.status_code == 404
    
    response = client.put("/productos/9999", json={"nombre": "Test", "precio": 10.0})
    assert response.status_code == 404
    
    response = client.delete("/productos/9999")
    assert response.status_code == 404