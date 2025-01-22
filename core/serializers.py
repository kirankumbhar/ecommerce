from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items']

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("An order should contain at least one item.")
        
        # Validate stock for each item
        for item in items:
            product = item['product']
            quantity = item['quantity']
            
            if quantity <= 0:
                raise serializers.ValidationError(f"Quantity must be positive for {product.name}")
            
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                )
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = sum(
            item['product'].price * item['quantity']
            for item in items_data
        )
        order = Order.objects.create(
            user=self.context['request'].user,
            total_price=total_amount
        )
        
        # Create order items and update stock
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            product.stock -= quantity
            product.save()
        
        return order