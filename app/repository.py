from typing import List, Optional, Dict, Any
from app.schemas import ProductoCreate, ProductoUpdate
import logging

logger = logging.getLogger(__name__)


class ProductoRepo:
    def __init__(self):
        self.db: List[Dict[str, Any]] = []
        self.counter = 1

    def listar(self) -> List[Dict[str, Any]]:
        return self.db.copy()

    def crear(self, data: ProductoCreate) -> Dict[str, Any]:
        producto = {"id": self.counter, "nombre": data.nombre, "precio": data.precio}
        self.counter += 1
        self.db.append(producto)
        logger.debug(f"Producto creado en repositorio: {producto}")
        return producto

    def obtener(self, prod_id: int) -> Optional[Dict[str, Any]]:
        for producto in self.db:
            if producto["id"] == prod_id:
                return producto
        return None

    def actualizar(
        self, prod_id: int, data: ProductoUpdate
    ) -> Optional[Dict[str, Any]]:
        producto = self.obtener(prod_id)
        if not producto:
            return None

        if data.nombre is not None:
            producto["nombre"] = data.nombre
        if data.precio is not None:
            producto["precio"] = data.precio

        logger.debug(f"Producto actualizado en repositorio: {producto}")
        return producto

    def eliminar(self, prod_id: int) -> bool:
        initial_length = len(self.db)
        self.db = [p for p in self.db if p["id"] != prod_id]
        was_deleted = len(self.db) < initial_length

        if was_deleted:
            logger.debug(f"Producto eliminado del repositorio: ID {prod_id}")

        return was_deleted
