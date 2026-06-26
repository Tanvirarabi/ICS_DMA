from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    etin = models.CharField(max_length=255, blank=True, null=True)
    vat_certificate = models.CharField(max_length=255, blank=True, null=True)
    incorporartion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = '1. Organizations'

    def __str__(self):
        return self.name

class Location(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=[('office', 'Office'), ('warehouse', 'Warehouse')])
    address = models.TextField()

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = '2. Locations'

    def __str__(self):
        return self.name

class Room(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = '3. Rooms'

    def __str__(self):
        return self.name

class StorageSpot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Storage Spot'
        verbose_name_plural = '4. Storage Spots'

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = '5. Suppliers'

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Raw Material'
        verbose_name_plural = '6. Raw Materials'

    def __str__(self):
        return self.name

class BOM(models.Model):
    name = models.CharField(max_length=255)
    raw_materials = models.ManyToManyField(RawMaterial, through='BOMItem')

    class Meta:
        verbose_name = 'BOM'
        verbose_name_plural = '7. BOM'

    def __str__(self):
        return self.name

class BOMItem(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = 'BOM Item'
        verbose_name_plural = '8. BOM Items'

    def __str__(self):
        return f"{self.raw_material.name} in {self.bom.name} - Quantity: {self.quantity}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = '9. Products'

    def __str__(self):
        return self.name

class RawMaterialInventory(models.Model):
    storage_spot = models.ForeignKey(StorageSpot, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = 'Raw Material Inventory'
        verbose_name_plural = '10. Raw Material Inventories'

    def __str__(self):
        return f"{self.raw_material} in {self.storage_spot}"

class FinishedProductInventory(models.Model):
    storage_spot = models.ForeignKey(StorageSpot, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = 'Finished Product Inventory'
        verbose_name_plural = '11. Finished Product Inventories'

    def __str__(self):
        return f"{self.product} in {self.storage_spot}"

class Production(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_materials_used = models.ManyToManyField(RawMaterial, through='ProductionRawMaterial')
    finished_product_quantity = models.FloatField()
    production_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Production'
        verbose_name_plural = '12. Productions'

    def __str__(self):
        return f"Production of {self.product} on {self.production_date}"

class ProductionRawMaterial(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_used = models.FloatField()

    class Meta:
        verbose_name = 'Production Raw Material'
        verbose_name_plural = '13. Production Raw Materials'

    def __str__(self):
        return f"{self.quantity_used} of {self.raw_material} used in {self.production}"

class MovementLog(models.Model):
    FROM_CHOICES = [
        ('raw_material', 'Raw Material'),
        ('production_line', 'Production Line'),
        ('finished_goods', 'Finished Goods'),
    ]

    TO_CHOICES = FROM_CHOICES

    timestamp = models.DateTimeField(auto_now_add=True)
    item_type = models.CharField(max_length=50, choices=[('raw_material', 'Raw Material'), ('product', 'Product')])
    item_id = models.IntegerField()
    from_location = models.CharField(max_length=50, choices=FROM_CHOICES)
    to_location = models.CharField(max_length=50, choices=TO_CHOICES)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Movement Log'
        verbose_name_plural = '14. Movement Logs'


    def __str__(self):
        return f"{self.item_type} {self.item_id} moved from {self.from_location} to {self.to_location}"
    


class BarcodeCategory(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Barcode Category'
        verbose_name_plural = 'Barcode Categories'

    def __str__(self):
        return self.title


class BarcodedProduct(models.Model):
    product_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, unique=True)
    product_location = models.CharField(max_length=1024, default="Shelf")
    category = models.ForeignKey(BarcodeCategory, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Barcoded Product'
        verbose_name_plural = 'Barcoded Products'

    def __str__(self):
        return self.product_name
