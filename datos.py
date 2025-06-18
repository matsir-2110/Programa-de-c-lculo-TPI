import json

productos = [
    {"nombre": "Detergente Líquido", "descripcion": "Detergente para ropa, 1L", "precio": 3000.00, "stock": 50},
    {"nombre": "Lavandina", "descripcion": "Lavandina concentrada, 1L", "precio": 4000.00, "stock": 75},
    {"nombre": "Limpiador Multiuso", "descripcion": "Limpiador para superficies, 500ml", "precio": 1500.00, "stock": 100},
    {"nombre": "Esponjas", "descripcion": "Paquete x 5 unidades", "precio": 2000.00, "stock": 200},
    {"nombre": "Guantes de Látex", "descripcion": "Talla M, paquete x 10", "precio": 1500.00, "stock": 40},
    {"nombre": "Desinfectante", "descripcion": "Desinfectante en spray, 600ml", "precio": 3000.00, "stock": 60},
    {"nombre": "Jabón Líquido", "descripcion": "Jabón para manos, 250ml", "precio": 5000.00, "stock": 80},
]

with open("productos.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, indent=4, ensure_ascii=False)