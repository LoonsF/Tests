import time
from fastapi.testclient import TestClient
from app.main import app

def test_e2e_full_producto_lifecycle():
    client = TestClient(app)
    producto_nombre = f"Producto E2E {int(time.time())}"
    
    response_get_inicial = client.get("/productos")
    assert response_get_inicial.status_code == 200
    initial_list = response_get_inicial.json()
    initial_count = len(initial_list)
    
    resp_create = client.post("/productos", json={"nombre": producto_nombre, "precio": 10.5})
    assert resp_create.status_code == 201
    producto_id = resp_create.json()["id"]
    
    resp_get = client.get(f"/productos/{producto_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["nombre"] == producto_nombre
    
    resp_upd = client.put(f"/productos/{producto_id}", json={"nombre": producto_nombre + "_Actualizado", "precio": 20.0})
    assert resp_upd.status_code == 200
    producto_actualizado = resp_upd.json()
    assert producto_actualizado["nombre"] == producto_nombre + "_Actualizado"
    assert producto_actualizado["precio"] == 20.0
    
    resp_del = client.delete(f"/productos/{producto_id}")
    assert resp_del.status_code == 200
    assert resp_del.json()["status"] == "ok"

def test_cliente_metodos():
    """Test para verificar que todos los métodos funcionan"""
    client = TestClient(app)
    
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    producto_data = {"nombre": "Test Cliente", "precio": 15.0}
    response = client.post("/productos", json=producto_data)
    assert response.status_code == 201
    producto_id = response.json()["id"]
    
    update_data = {"nombre": "Test Cliente Actualizado", "precio": 25.0}
    response = client.put(f"/productos/{producto_id}", json=update_data)
    assert response.status_code == 200
    
    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200