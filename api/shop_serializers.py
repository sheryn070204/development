from rest_framework import serializers
from .shop_models import Product, CartItem, Payment

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'image_url']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            # Manually construct the URL with the port
            base_url = "http://172.17.100.14:3342/cuabo2"
            relative_url = instance.image.url
            representation['image'] = f"{base_url}{relative_url}"
        else:
            representation['image'] = None
        return representation

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return f"http://172.17.100.14:3342/cuabo2{obj.image.url}"
        return None

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return str(obj.quantity * obj.product.price)

class PaymentSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Payment
        fields = [
            'id', 
            'name', 
            'email', 
            'address', 
            'avatar',
            'payment_method', 
            'total_amount', 
            'products',
            'created_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.avatar:
            # Manually construct the URL with the port
            base_url = "http://172.17.100.14:3342/cuabo2"
            relative_url = instance.avatar.url
            representation['avatar'] = f"{base_url}{relative_url}"
        else:
            representation['avatar'] = None
        return representation
