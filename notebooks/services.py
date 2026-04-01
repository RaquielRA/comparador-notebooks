import httpx
import re
from django.templatetags.static import static

IMAGE_FALLBACK = static('notebooks/static/img/image.png')


class LaptopService:
    @staticmethod
    async def buscar_notebooks(query="", p_min=0, p_max=20000, ram=None, ssd=None, cpu=None, gpu=None):
        # Base de dados simulada com modelos reais do mercado brasileiro
        base_dados = [
            {"id": "L1", "marca": "Dell", "nome": "Dell G15 5530", "preco": 5899.00, "cpu": "i5-13450HX", "gpu": "RTX 3050", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/51p1Lh5fS0L._AC_SL1000_.jpg"},
            {"id": "L2", "marca": "Apple", "nome": "MacBook Air M2", "preco": 8200.00, "cpu": "Apple M2", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L3", "marca": "Acer", "nome": "Acer Nitro 5 AN515", "preco": 4350.00, "cpu": "i7-11800H", "gpu": "RTX 3050", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/61S-fJ4-QAL._AC_SL1000_.jpg"},
            {"id": "L4", "marca": "Lenovo", "nome": "Legion Slim 5i", "preco": 7499.00, "cpu": "i7-13700H", "gpu": "RTX 4060", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/616vS-tGvWL._AC_SL1000_.jpg"},
            {"id": "L5", "marca": "Samsung", "nome": "Galaxy Book3 Ultra", "preco": 12999.00, "cpu": "i9-13900H", "gpu": "RTX 4070", "ram": "32GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L6", "marca": "Asus", "nome": "ROG Strix G16", "preco": 8999.00, "cpu": "i7-13650HX", "gpu": "RTX 4060", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L7", "marca": "HP", "nome": "Victus 15", "preco": 4799.00, "cpu": "i5-12450H", "gpu": "RTX 3050", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L8", "marca": "Lenovo", "nome": "IdeaPad Gaming 3", "preco": 3999.00, "cpu": "Ryzen 5 5600H", "gpu": "GTX 1650", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71K7R9bLqzL._AC_SL1500_.jpg"},
            {"id": "L9", "marca": "Dell", "nome": "Inspiron 15 3520", "preco": 3299.00, "cpu": "i5-1235U", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L10", "marca": "Apple", "nome": "MacBook Pro M3", "preco": 14999.00, "cpu": "Apple M3", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L11", "marca": "Acer", "nome": "Aspire 5", "preco": 2999.00, "cpu": "i5-1135G7", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L12", "marca": "Asus", "nome": "VivoBook 15", "preco": 2799.00, "cpu": "Ryzen 5 5500U", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L13", "marca": "HP", "nome": "Pavilion 14", "preco": 3599.00, "cpu": "i5-1240P", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L14", "marca": "Samsung", "nome": "Galaxy Book2", "preco": 4199.00, "cpu": "i5-1240P", "gpu": "Integrated", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/61l7E6bVnIL._AC_SL1500_.jpg"},
            {"id": "L15", "marca": "Lenovo", "nome": "ThinkPad E14", "preco": 5299.00, "cpu": "Ryzen 7 5700U", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71p0f9rZLPL._AC_SL1500_.jpg"},
            {"id": "L16", "marca": "Dell", "nome": "XPS 13 Plus", "preco": 11999.00, "cpu": "i7-1360P", "gpu": "Integrated", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/61eA1mK0S+L._AC_SL1500_.jpg"},
            {"id": "L17", "marca": "Asus", "nome": "ZenBook 14", "preco": 6999.00, "cpu": "i7-1260P", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L18", "marca": "Acer", "nome": "Swift 3", "preco": 4799.00, "cpu": "Ryzen 7 5700U", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L19", "marca": "HP", "nome": "Envy x360", "preco": 6499.00, "cpu": "Ryzen 7 5800U", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L20", "marca": "Lenovo", "nome": "Yoga Slim 7", "preco": 6999.00, "cpu": "i7-1260P", "gpu": "Integrated", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/71K7R9bLqzL._AC_SL1500_.jpg"},
            {"id": "L21", "marca": "Dell", "nome": "Alienware M16", "preco": 15999.00, "cpu": "i9-13900HX", "gpu": "RTX 4080", "ram": "32GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/71p0f9rZLPL._AC_SL1500_.jpg"},
            {"id": "L22", "marca": "Asus", "nome": "TUF Gaming F15", "preco": 5599.00, "cpu": "i7-12700H", "gpu": "RTX 3050", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L23", "marca": "Acer", "nome": "Predator Helios 300", "preco": 8999.00, "cpu": "i7-12700H", "gpu": "RTX 4060", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/61S-fJ4-QAL._AC_SL1000_.jpg"},
            {"id": "L24", "marca": "Lenovo", "nome": "Legion 5", "preco": 7999.00, "cpu": "Ryzen 7 6800H", "gpu": "RTX 3060", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/616vS-tGvWL._AC_SL1000_.jpg"},
            {"id": "L25", "marca": "Samsung", "nome": "Galaxy Book Odyssey", "preco": 6999.00, "cpu": "i7-11600H", "gpu": "RTX 3050 Ti", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L26", "marca": "HP", "nome": "Omen 16", "preco": 9499.00, "cpu": "i7-13700HX", "gpu": "RTX 4060", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L27", "marca": "Dell", "nome": "G3 15", "preco": 4599.00, "cpu": "i5-10300H", "gpu": "GTX 1650", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/51p1Lh5fS0L._AC_SL1000_.jpg"},
            {"id": "L28", "marca": "Lenovo", "nome": "IdeaPad 3", "preco": 2499.00, "cpu": "Ryzen 3 5300U", "gpu": "Integrated", "ram": "4GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71K7R9bLqzL._AC_SL1500_.jpg"},
            {"id": "L29", "marca": "Acer", "nome": "Aspire 3", "preco": 2299.00, "cpu": "i3-1115G4", "gpu": "Integrated", "ram": "4GB", "ssd": "128GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L30", "marca": "Asus", "nome": "VivoBook Go 14", "preco": 1999.00, "cpu": "Ryzen 3 3250U", "gpu": "Integrated", "ram": "4GB", "ssd": "128GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L31", "marca": "Samsung", "nome": "Galaxy Book Go", "preco": 1799.00, "cpu": "Snapdragon 7c", "gpu": "Integrated", "ram": "4GB", "ssd": "128GB", "foto": "https://m.media-amazon.com/images/I/61l7E6bVnIL._AC_SL1500_.jpg"},
            {"id": "L32", "marca": "Apple", "nome": "MacBook Air M1", "preco": 6999.00, "cpu": "Apple M1", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L33", "marca": "Dell", "nome": "Latitude 5440", "preco": 8499.00, "cpu": "i7-1355U", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L34", "marca": "HP", "nome": "EliteBook 840", "preco": 9999.00, "cpu": "i7-1360P", "gpu": "Integrated", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L35", "marca": "Lenovo", "nome": "ThinkBook 15", "preco": 4899.00, "cpu": "i5-1235U", "gpu": "Integrated", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71p0f9rZLPL._AC_SL1500_.jpg"},
            {"id": "L36", "marca": "Asus", "nome": "ExpertBook B1", "preco": 3999.00, "cpu": "i5-1135G7", "gpu": "Integrated", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L37", "marca": "Acer", "nome": "TravelMate P2", "preco": 4299.00, "cpu": "i5-1240P", "gpu": "Integrated", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L38", "marca": "Dell", "nome": "Vostro 3510", "preco": 3199.00, "cpu": "i3-1115G4", "gpu": "Integrated", "ram": "8GB", "ssd": "256GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L41", "marca": "Asus", "nome": "ROG Zephyrus G14", "preco": 10999.00, "cpu": "Ryzen 9 6900HS", "gpu": "RTX 4060", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L42", "marca": "Acer", "nome": "Nitro 16", "preco": 7999.00, "cpu": "Ryzen 7 7735HS", "gpu": "RTX 4050", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/61S-fJ4-QAL._AC_SL1000_.jpg"},
            {"id": "L43", "marca": "HP", "nome": "Victus 16", "preco": 6799.00, "cpu": "Ryzen 7 6800H", "gpu": "RTX 3050", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"},
            {"id": "L44", "marca": "Dell", "nome": "G16 Gaming", "preco": 8599.00, "cpu": "i7-13650HX", "gpu": "RTX 4060", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/51p1Lh5fS0L._AC_SL1000_.jpg"},
            {"id": "L45", "marca": "Lenovo", "nome": "Legion Pro 5", "preco": 9999.00, "cpu": "Ryzen 7 7745HX", "gpu": "RTX 4070", "ram": "32GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/616vS-tGvWL._AC_SL1000_.jpg"},
            {"id": "L46", "marca": "Samsung", "nome": "Galaxy Book4 Pro", "preco": 11999.00, "cpu": "i7-155H", "gpu": "Integrated", "ram": "16GB", "ssd": "1TB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L47", "marca": "Apple", "nome": "MacBook Pro M2 Pro", "preco": 17999.00, "cpu": "Apple M2 Pro", "gpu": "Integrated", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L48", "marca": "Acer", "nome": "Swift X", "preco": 6999.00, "cpu": "Ryzen 7 5800U", "gpu": "RTX 3050", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71vvXGmdKWL._AC_SL1500_.jpg"},
            {"id": "L49", "marca": "Asus", "nome": "TUF Dash F15", "preco": 6499.00, "cpu": "i7-12650H", "gpu": "RTX 3050 Ti", "ram": "16GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/719C6bJv8jL._AC_SL1500_.jpg"},
            {"id": "L50", "marca": "HP", "nome": "Pavilion Gaming 15", "preco": 4999.00, "cpu": "Ryzen 5 5600H", "gpu": "GTX 1650", "ram": "8GB", "ssd": "512GB", "foto": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg"}
        ]

        lista_filtrada = []

        IMAGE_FALLBACK = static('img/image.png')

        for item in base_dados:
            # 1. Filtro por Nome/Marca
            if query and query.lower() not in item['nome'].lower() and query.lower() not in item['marca'].lower():
                continue
            
            # 2. Filtro por Faixa de Preço (Corrigido para usar 'item')
            try:
                if p_min and item['preco'] < float(p_min):
                    continue
                if p_max and item['preco'] > float(p_max):
                    continue
            except ValueError:
                pass 
                
            # 3. Filtro por Hardware (CPU, GPU, RAM, SSD)
            if cpu and cpu.lower() not in item['cpu'].lower(): continue
            if gpu and gpu.lower() not in item['gpu'].lower(): continue
            if ram and ram.lower() not in item['ram'].lower(): continue
            if ssd and ssd.lower() not in item['ssd'].lower(): continue

            # Mapeamento Final TechHub
            lista_filtrada.append({
                'id': item['id'],
                'marca': item['marca'],
                'nome': item['nome'],
                'preco': f"{item['preco']:.2f}",
                # Lógica de Imagem Genérica (Fallback)
                'foto': item.get('foto') if item.get('foto') else IMAGE_FALLBACK,
                'cpu': item['cpu'],
                'gpu': item['gpu'],
                'ram': item['ram'],
                'ssd': item['ssd'],
                'specs': {
                    'Processador': item['cpu'],
                    'RAM': item['ram'],
                    'SSD': item['ssd'],
                    'Descricao': f"Dispositivo TechHub: {item['marca']} equipado com {item['cpu']} e {item['gpu']}."
                }
            })
            
        return lista_filtrada