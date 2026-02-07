
from shop.models import Category, Product, Review
from django.utils import timezone
import random
def run():
    blocks = [{"category": "Electronics", "slug": "electronics", "items": [{"name": "NovaPhone X1", "slug": "novaphone-x1", "price": 699, "img": "https://picsum.photos/seed/phone/640/480", "desc": "Powerful smartphone with long-lasting battery and bright OLED display."}, {"name": "SonicBuds Pro", "slug": "sonicbuds-pro", "price": 129, "img": "https://picsum.photos/seed/buds/640/480", "desc": "Noise-cancelling earbuds with clear bass and comfortable fit."}, {"name": "SkyCam 4K Drone", "slug": "skycam-4k-drone", "price": 399, "img": "https://picsum.photos/seed/drone/640/480", "desc": "4K aerial drone with image stabilization and long flight time."}]}, {"category": "Books", "slug": "books", "items": [{"name": "Deep Learning with Python", "slug": "dl-with-python", "price": 49, "img": "https://picsum.photos/seed/book1/640/480", "desc": "Hands-on guide to deep learning and neural networks."}, {"name": "Recommender Systems Handbook", "slug": "rs-handbook", "price": 89, "img": "https://picsum.photos/seed/book2/640/480", "desc": "Comprehensive coverage of RS algorithms and applications."}]}, {"category": "Clothes", "slug": "clothes", "items": [{"name": "AeroFit Running Tee", "slug": "aerofit-tee", "price": 29, "img": "https://picsum.photos/seed/shirt/640/480", "desc": "Lightweight breathable t-shirt for workouts."}, {"name": "ComfyFlex Hoodie", "slug": "comfyflex-hoodie", "price": 59, "img": "https://picsum.photos/seed/hoodie/640/480", "desc": "Cozy hoodie with soft inner lining."}]}]
    for b in blocks:
        cat, _ = Category.objects.get_or_create(name=b['category'], slug=b['slug'])
        for it in b['items']:
            p, _ = Product.objects.get_or_create(
                category=cat, name=it['name'], slug=it['slug'],
                defaults={'price':it['price'], 'description':it['desc'], 'image_url':it['img']}
            )
            samples = [
                "Absolutely love it! Battery lasts forever.",
                "Great quality and value for money.",
                "Solid performance, decent build.",
                "Exceeded expectations, highly recommend.",
                "Good but could be better in some areas.",
                "Amazing!!! Best product ever!!!",
                "Wow wow wow fantastic incredible awesome!",
                "Buy this now!!! Life changing!!!"
            ]
            for i in range(8):
                Review.objects.create(product=p, user=None, rating=random.randint(3,5),
                    text=random.choice(samples), created_at=timezone.now())
    print("Sample data loaded.")
