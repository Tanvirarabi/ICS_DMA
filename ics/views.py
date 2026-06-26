from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import RawMaterialInventory, FinishedProductInventory, Production, Product, Organization
from .serializers import RawMaterialInventorySerializer, FinishedProductInventorySerializer, ProductionSerializer
from .models import RawMaterialInventory, FinishedProductInventory, MovementLog, BarcodedProduct, BarcodeCategory
from .serializers import MovementLogSerializer, OrganizationSerializer, BarcodedProductSerializer, BarcodeCategorySerializer


class OrganizationListCreateAPIView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Organization List',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Organization Created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Organization Creation Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class OrganizationDetailAPIView(APIView):
    permission_classes = (AllowAny, )
    def get_object(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Organization Detail',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Organization Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Organization Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Organization Partially Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Organization Partial Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        organization = self.get_object(pk)
        organization.delete()
        response = {
            'success': 'True',
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'Organization Deleted',
            'data': {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class RawMaterialInventoryListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        inventories = RawMaterialInventory.objects.all()
        serializer = RawMaterialInventorySerializer(inventories, many=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Raw Material Inventory List',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RawMaterialInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Raw Material Inventory Created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Raw Material Inventory Creation Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RawMaterialInventoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return RawMaterialInventory.objects.get(pk=pk)
        except RawMaterialInventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        serializer = RawMaterialInventorySerializer(inventory)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Raw Material Inventory Detail',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        serializer = RawMaterialInventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Raw Material Inventory Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Raw Material Inventory Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        inventory.delete()
        response = {
            'success': 'True',
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'Raw Material Inventory Deleted',
            'data': {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class FinishedProductInventoryListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        inventories = FinishedProductInventory.objects.all()
        serializer = FinishedProductInventorySerializer(inventories, many=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Finished Product Inventory List',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FinishedProductInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Finished Product Inventory Created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Finished Product Inventory Creation Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class FinishedProductInventoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return FinishedProductInventory.objects.get(pk=pk)
        except FinishedProductInventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        serializer = FinishedProductInventorySerializer(inventory)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Finished Product Inventory Detail',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        serializer = FinishedProductInventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Finished Product Inventory Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Finished Product Inventory Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        inventory = self.get_object(pk)
        inventory.delete()
        response = {
            'success': 'True',
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'Finished Product Inventory Deleted',
            'data': {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class ProductionListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        productions = Production.objects.all()
        serializer = ProductionSerializer(productions, many=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Production List',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Production Created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Production Creation Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ProductionDetailView(APIView):
    def get_object(self, pk):
        try:
            return Production.objects.get(pk=pk)
        except Production.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        production = self.get_object(pk)
        serializer = ProductionSerializer(production)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Production Detail',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        production = self.get_object(pk)
        serializer = ProductionSerializer(production, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Production Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Production Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        production = self.get_object(pk)
        production.delete()
        response = {
            'success': 'True',
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'Production Deleted',
            'data': {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class MovementLogListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        logs = MovementLog.objects.all()
        serializer = MovementLogSerializer(logs, many=True)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Movement Log List',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MovementLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'Movement Log Created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Movement Log Creation Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MovementLogDetailView(APIView):
    def get_object(self, pk):
        try:
            return MovementLog.objects.get(pk=pk)
        except MovementLog.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        log = self.get_object(pk)
        serializer = MovementLogSerializer(log)
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'Movement Log Detail',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        log = self.get_object(pk)
        serializer = MovementLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Movement Log Updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': 'False',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Movement Log Update Failed',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        log = self.get_object(pk)
        log.delete()
        response = {
            'success': 'True',
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'Movement Log Deleted',
            'data': {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class MoveToProductionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        items = request.data.get('items', [])

        for item in items:
            item_type = item.get('type')
            item_id = item.get('id')
            quantity = item.get('quantity')

            if item_type == 'product':
                product = get_object_or_404(Product, id=item_id)
                bom = product.bom

                for bom_item in bom.bomitem_set.all():
                    raw_material = bom_item.raw_material
                    required_quantity = bom_item.quantity * quantity

                    raw_material_inventory = RawMaterialInventory.objects.get(raw_material=raw_material)
                    if raw_material_inventory.quantity >= required_quantity:
                        raw_material_inventory.quantity -= required_quantity
                        raw_material_inventory.save()

                        MovementLog.objects.create(
                            item_type='raw_material',
                            item_id=raw_material.id,
                            from_location='raw_material',
                            to_location='production_line',
                            quantity=required_quantity
                        )

                Production.objects.create(
                    product=product,
                    finished_product_quantity=quantity
                )

                MovementLog.objects.create(
                    item_type='product',
                    item_id=product.id,
                    from_location='raw_material',
                    to_location='production_line',
                    quantity=quantity
                )

        return Response({'status': 'success'})


class MoveToFinishedGoodsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        items = request.data.get('items', [])

        for item in items:
            item_type = item.get('type')
            item_id = item.get('id')
            quantity = item.get('quantity')

            if item_type == 'product':
                production = get_object_or_404(Production, product_id=item_id)
                if production.finished_product_quantity >= quantity:
                    production.finished_product_quantity -= quantity
                    production.save()

                    finished_product_inventory, created = FinishedProductInventory.objects.get_or_create(product_id=item_id)
                    finished_product_inventory.quantity += quantity
                    finished_product_inventory.save()

                    MovementLog.objects.create(
                        item_type='product',
                        item_id=item_id,
                        from_location='production_line',
                        to_location='finished_goods',
                        quantity=quantity
                    )

        return Response({'status': 'success'})


class ReturnToRawMaterialsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        items = request.data.get('items', [])

        for item in items:
            item_type = item.get('type')
            item_id = item.get('id')
            quantity = item.get('quantity')

            if item_type == 'product':
                product = get_object_or_404(Product, id=item_id)
                bom = product.bom

                for bom_item in bom.bomitem_set.all():
                    raw_material = bom_item.raw_material
                    required_quantity = bom_item.quantity * quantity

                    raw_material_inventory, created = RawMaterialInventory.objects.get_or_create(raw_material=raw_material)
                    raw_material_inventory.quantity += required_quantity
                    raw_material_inventory.save()

                    MovementLog.objects.create(
                        item_type='raw_material',
                        item_id=raw_material.id,
                        from_location='production_line',
                        to_location='raw_material',
                        quantity=required_quantity
                    )

                production = get_object_or_404(Production, product=product)
                production.finished_product_quantity -= quantity
                production.save()

                MovementLog.objects.create(
                    item_type='product',
                    item_id=product.id,
                    from_location='production_line',
                    to_location='raw_material',
                    quantity=quantity
                )

        return Response({'status': 'success'})


class FindProductByBarcodeAPIView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        barcode = request.data.get('barcode')
        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "API Successfully Parsed.",
            "user_message": "",
            "data": []
        }
        if not barcode:
            response["status_code"] = status.HTTP_400_BAD_REQUEST
            response['message'] = "Barcode is required."
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = BarcodedProduct.objects.filter(barcode=barcode).first()
            if product is not None:
                serializer = BarcodedProductSerializer(product)
                response['user_message'] = f"{product.product_name} is in {product.product_location}"
                response['message'] = "Product found."
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['message'] = "Product not found."
                response["status_code"] = status.HTTP_404_NOT_FOUND
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except:
            response['message'] = "Something went wrong."
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        

class BarcodedProductListAPIView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):

        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Product List",
            "user_message": "",
            "data": []
        }

        try:
            barcoded_products = BarcodedProduct.objects.all()
            serializer = BarcodedProductSerializer(barcoded_products, many=True)
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except:
            response['message'] = "Something went wrong."
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class BarcodeCategoryListAPIView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        categories = BarcodeCategory.objects.all()
        serializer = BarcodeCategorySerializer(categories, many=True)
        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Categories List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    

class RegisterBarcodedProductAPIView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = BarcodedProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "status_code": status.HTTP_201_CREATED,
                "message": "Product registered successfully.",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Product registration failed.",
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        