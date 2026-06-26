from rest_framework import serializers
from .models import RawMaterialInventory, FinishedProductInventory, Production, MovementLog, Organization, BarcodedProduct, BarcodeCategory


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            'name',
            'description',
            'website',
            'etin',
            'vat_certificate',
            'incorporartion'
        ]


class RawMaterialInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialInventory
        fields = '__all__'

class FinishedProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProductInventory
        fields = '__all__'

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'

class MovementLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementLog
        fields = '__all__'


class BarcodeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BarcodeCategory
        fields = ['id', 'title']


class BarcodedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarcodedProduct
        fields = [
            'id',
            'barcode',
            'product_name',
            'product_location',
            'category'
        ]
