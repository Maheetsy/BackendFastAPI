# Importar las clases de product.py para que estén disponibles
from .product import (
    Product,
    ProductBase,
    ProductCreate,
    ProductUpdate,
    StockAdjustment,
)

# Importar las clases de category.py para que estén disponibles
# (Asegúrate de haber creado el archivo app/schemas/category.py)
from .category import Category, CategoryBase, CategoryCreate