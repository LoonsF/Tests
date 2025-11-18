from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ProductoCreate, ProductoUpdate, Producto
from app.repository import ProductoRepo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Productos",
    description="Una API RESTful para gestionar productos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = ProductoRepo()


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Productos"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/productos", response_model=list[Producto])
def listar_productos():
    try:
        productos = repo.listar()
        logger.info(f"Listados {len(productos)} productos")
        return productos
    except Exception as e:
        logger.error(f"Error al listar productos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )


@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCreate):
    try:
        producto = repo.crear(data)
        logger.info(f"Producto creado: {producto}")
        return producto
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )


@app.get("/productos/{prod_id}", response_model=Producto)
def obtener_producto(prod_id: int):
    producto = repo.obtener(prod_id)
    if not producto:
        logger.warning(f"Producto no encontrado: ID {prod_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


@app.put("/productos/{prod_id}", response_model=Producto)
def actualizar_producto(prod_id: int, data: ProductoUpdate):
    producto_actualizado = repo.actualizar(prod_id, data)
    if not producto_actualizado:
        logger.warning(f"Producto no encontrado para actualizar: ID {prod_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    logger.info(f"Producto actualizado: {producto_actualizado}")
    return producto_actualizado


@app.delete("/productos/{prod_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(prod_id: int):
    producto = repo.obtener(prod_id)
    if not producto:
        logger.warning(f"Producto no encontrado para eliminar: ID {prod_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )

    repo.eliminar(prod_id)
    logger.info(f"Producto eliminado: ID {prod_id}")
    return {
        "status": "ok",
        "message": f"Producto {prod_id} eliminado correctamente",
        "id_eliminado": prod_id,
    }
