from django.contrib import admin
from .models import (
    RawMaterialInventory, FinishedProductInventory, Production, MovementLog, Product,
    Organization, Location, Room, StorageSpot, Supplier, BOM, RawMaterial, BOMItem, ProductionRawMaterial,
    BarcodedProduct, BarcodeCategory
)

class RawMaterialInventoryAdmin(admin.ModelAdmin):
    list_display = ('raw_material', 'quantity', 'storage_spot')
    search_fields = ('raw_material__name',)

class FinishedProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'storage_spot')
    search_fields = ('product__name',)

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('product', 'finished_product_quantity', 'production_date')
    search_fields = ('product__name',)
    list_filter = ('production_date',)

class MovementLogAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_id', 'quantity', 'from_location', 'to_location', 'timestamp')
    search_fields = ('item_type', 'from_location', 'to_location')
    list_filter = ('timestamp',)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'location_type')
    search_fields = ('name', 'organization__name')
    list_filter = ('location_type',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location__name')

class StorageSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'room')
    search_fields = ('name', 'room__name')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)

class BOMAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'unit_price')
    search_fields = ('name', 'supplier__name')

class BOMItemAdmin(admin.ModelAdmin):
    list_display = ('bom', 'raw_material', 'quantity')
    search_fields = ('bom__name', 'raw_material__name')

class ProductionRawMaterialAdmin(admin.ModelAdmin):
    list_display = ('production', 'raw_material', 'quantity_used')
    search_fields = ('production__product__name', 'raw_material__name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'bom')
    search_fields = ('name', 'bom__name')

class BarcodedProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'barcode', 'product_location')
    search_fields = ('product_name', 'barcode')

class BarcodeCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)

admin.site.register(Product, ProductAdmin)

admin.site.register(BOMItem, BOMItemAdmin)
admin.site.register(ProductionRawMaterial, ProductionRawMaterialAdmin)

admin.site.register(RawMaterialInventory, RawMaterialInventoryAdmin)
admin.site.register(FinishedProductInventory, FinishedProductInventoryAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(MovementLog, MovementLogAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(StorageSpot, StorageSpotAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(BOM, BOMAdmin)
admin.site.register(RawMaterial, RawMaterialAdmin)
admin.site.register(BarcodedProduct, BarcodedProductAdmin)
admin.site.register(BarcodeCategory, BarcodeCategoryAdmin)
