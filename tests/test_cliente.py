import time
from app.main import app
from tests.utils import TestCliente

cliente = TestCliente(app)

def test_e2e_full_producto_lifecycle():
    producto_nombre = f"Producto E2E {int(time.time())}"
    
    response_get_inicial = cliente.get("/productos")
    assert response_get_inicial.status_code == 200
    initial_list = response_get_inicial.json()
    initial_count = len(initial_list)
    
    print(f"Productos iniciales: {initial_count}")
    print(f"Lista inicial: {initial_list}")
    print("Iniciando ciclo completo de producto...")
    
    resp_create = cliente.post("/productos", json={"nombre": producto_nombre, "precio": 10.5})
    assert resp_create.status_code == 201
    producto_id = resp_create.json()["id"]
    print(f"Producto creado con ID: {producto_id}")
    response_despues_crear = cliente.get("/productos")
    assert len(response_despues_crear.json()) == initial_count + 1
    
    resp_get = cliente.get(f"/productos/{producto_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["nombre"] == producto_nombre
    print(f"Producto obtenido: {resp_get.json()}")
    
    resp_upd = cliente.put(f"/productos/{producto_id}", json={"nombre": producto_nombre + "_Actualizado", "precio": 20.0})
    assert resp_upd.status_code == 200
    producto_actualizado = resp_upd.json()
    assert producto_actualizado["nombre"] == producto_nombre + "_Actualizado"
    assert producto_actualizado["precio"] == 20.0
    print(f"Producto actualizado: {producto_actualizado}")
    
    resp_del = cliente.delete(f"/productos/{producto_id}")
    assert resp_del.status_code == 200
    assert resp_del.json()["status"] == "ok"
    print(f"Producto eliminado: {resp_del.json()}")
    resp_get_final = cliente.get(f"/productos/{producto_id}")
    assert resp_get_final.status_code == 404
    
    response_final = cliente.get("/productos")
    assert len(response_final.json()) == initial_count
    print(f"Productos finales: {len(response_final.json())}")
    print("Ciclo completo de producto finalizado exitosamente")

def test_cliente_metodos():
    """Test para verificar que todos los métodos del cliente funcionan"""
    
    response = cliente.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    producto_data = {"nombre": "Test Cliente", "precio": 15.0}
    response = cliente.post("/productos", json=producto_data)
    assert response.status_code == 201
    producto_id = response.json()["id"]
    
    update_data = {"nombre": "Test Cliente Actualizado", "precio": 25.0}
    response = cliente.put(f"/productos/{producto_id}", json=update_data)
    assert response.status_code == 200
    
    response = cliente.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    
    print("Todos los métodos del TestCliente funcionan correctamente")