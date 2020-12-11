from rest_framework import serializers
from django.contrib.auth.models import User, AnonymousUser
from django.db import transaction
from .models import Product
from .models import ProductGroup
from .models import OrderItem
from .models import Order
from .models import ShippingAddress
from .models import Country
from .models import Review


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=ProductGroup.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'group', 'name', 'image', 'description', 'price', 'sale', 'sale_price', 'rating']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Method overridden to set user password.
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']


class ShippingAddressSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = ['id', 'order', 'first_name', 'last_name', 'email', 'country', 'address', 'phone']


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    price = Product.price
    sale_price = Product.sale_price

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'sale_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    shipping_address = ShippingAddressSerializer(many=False)
    order_items = OrderItemSerializer(many=True)
    subtotal = serializers.ReadOnlyField(source='get_subtotal')
    total = serializers.ReadOnlyField(source='get_total')

    class Meta:
        model = Order
        fields = ['id', 'order_created', 'order_updated', 'subtotal', 'total', 'shipping_address', 'order_status',
                  'order_items', 'owner']

    # With Order should be created Shipping address and Order items, so we need to create their in DB.
    def create(self, validated_data):
        shipping_address_data = validated_data.pop('shipping_address')
        items_data = validated_data.pop('order_items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            ShippingAddress.objects.create(order=order, **shipping_address_data)
            for item in items_data:
                OrderItem.objects.create(order=order, **item)
            return order

    # If the request has changed data for shipping address or items it has to be updated in DB.
    def update(self, instance, validated_data):
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()
        # Check if shipping address changed save it in DB and set it to instance.
        if validated_data.get('shipping_address', None):
            shipping_address_data = validated_data.pop('shipping_address')
            shipping_address = instance.shipping_address
            for attr_name, value in shipping_address_data.items():
                setattr(shipping_address, attr_name, value)
            shipping_address.save()
            instance.shipping_address = shipping_address

        # Check if order items changed save it in DB and set it to instance.
        if validated_data.get('order_items', None):
            order_items_data = validated_data.pop('order_items')
            with transaction.atomic():
                # Here from all items in current DB will be dropped and new items will be saved.
                OrderItem.objects.filter(order__exact=instance.id).delete()
                updated_items = []
                for item in order_items_data:
                    updated_items.append(OrderItem.objects.create(order=instance, **item))
                instance.order_items.set(updated_items)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'review']
