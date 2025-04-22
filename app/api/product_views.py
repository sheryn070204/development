from rest_framework.decorators import api_view
from rest_framework.response import Response
from .product_models import Product, CartItem, Checkout
from .product_serializers import ProductSerializer, CartItemSerializer, CheckoutSerializer

@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['POST'])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def view_cart(request):
    cart_items = CartItem.objects.all()
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def checkout(request):
    serializer = CheckoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        cart_items = CartItem.objects.all()
        for item in cart_items:
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                return Response({"error": f"Not enough stock for {product.name}"}, status=400)

        CartItem.objects.all().delete()
        return Response({'message': 'Checkout successful'})
    return Response(serializer.errors, status=400)