from django.core.management.base import BaseCommand
from api.models import Product

class Command(BaseCommand):
    help = "Seed database with initial products for Inkify Creations"

    def handle(self, *args, **options):
        # Initial products matching app.js catalog
        products_data = [
            {
                "id": 1,
                "name": "Premium T-Shirt",
                "category": "Apparel",
                "original_price": 500.00,
                "price": 399.00,
                "cart_price": None,
                "image": "assets/tshirt.png",
                "description": "Ultra-soft 220 GSM combed cotton. Shown customized with bold neon 'Inkify Creations' typography."
            },
            {
                "id": 2,
                "name": "Executive Polo T-Shirt",
                "category": "Apparel",
                "original_price": 600.00,
                "price": 499.00,
                "cart_price": None,
                "image": "assets/polo tshirt.png",
                "description": "Executive honeycomb knit polo. Shown customized with elegant cursive 'Yours Story' or 'Your Name' embroidery."
            },
            {
                "id": 3,
                "name": "Structured Snapback Cap",
                "category": "Headwear",
                "original_price": 350.00,
                "price": 299.00,
                "cart_price": 299.00,
                "image": "assets/cap.png",
                "description": "Structured 6-panel snapback cap. Shown customized with stylized 'Your Hero' vectors in glowing purple."
            },
            {
                "id": 4,
                "name": "High-Gloss Ceramic Mug",
                "category": "Drinkware",
                "original_price": 350.00,
                "price": 239.00,
                "cart_price": 239.00,
                "image": "assets/mugcat.png",
                "description": "High-gloss ceramic mug. Shown customized with Ghibli-inspired family artwork printing."
            },
            {
                "id": 5,
                "name": "The Purple Gifting Set",
                "category": "Signature Bundle",
                "original_price": 1500.00,
                "price": 1149.00,
                "cart_price": 1199.00,
                "image": "assets/gift_box.png",
                "description": "Premium velvet-feel signature gift box containing T-Shirt, Polo, Mug, & Cap printed with your story."
            }
        ]

        for item in products_data:
            product, created = Product.objects.get_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "category": item["category"],
                    "original_price": item["original_price"],
                    "price": item["price"],
                    "cart_price": item["cart_price"],
                    "image": item["image"],
                    "description": item["description"]
                }
            )
            
            if not created:
                # Update attributes if already exists
                product.name = item["name"]
                product.category = item["category"]
                product.original_price = item["original_price"]
                product.price = item["price"]
                product.cart_price = item["cart_price"]
                product.image = item["image"]
                product.description = item["description"]
                product.save()
                self.stdout.write(self.style.SUCCESS(f"Updated product: {product.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))

        self.stdout.write(self.style.SUCCESS("Database seeded with products successfully."))
