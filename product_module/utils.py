from .models import Product

def searchProducts(request):
    if request.method == "GET":
        searched = request.GET['q']
        products = Product.objects.filter(title__icontains=searched)

    return products,searched