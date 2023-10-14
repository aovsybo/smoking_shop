from rest_framework import serializers

from products.models import Product, Category


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "producer",
            "slug",
            "description",
            "price",
            "image",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "slug",
            "get_absolute_url",
            "producer",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.category = validated_data.get("category", instance.category)
        instance.producer = validated_data.get("producer", instance.producer)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance


class CategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
            "products",
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance
