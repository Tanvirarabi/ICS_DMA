from django.urls import path
from django.contrib import admin
from .views import (
    MoveToProductionAPIView, MoveToFinishedGoodsAPIView, ReturnToRawMaterialsAPIView,
    RawMaterialInventoryListCreateView, RawMaterialInventoryDetailView,
    FinishedProductInventoryListCreateView, FinishedProductInventoryDetailView,
    ProductionListCreateView, ProductionDetailView,
    MovementLogListCreateView, MovementLogDetailView,
    OrganizationListCreateAPIView, OrganizationDetailAPIView, FindProductByBarcodeAPIView, BarcodedProductListAPIView,
    BarcodeCategoryListAPIView, RegisterBarcodedProductAPIView
)

urlpatterns = [
    
     path('admin/', admin.site.urls),

    path('organizations/', OrganizationListCreateAPIView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailAPIView.as_view(), name='organization-detail'),

    path('raw_material_inventory/', RawMaterialInventoryListCreateView.as_view(), name='raw_material_inventory_list_create'),
    path('raw_material_inventory/<int:pk>/', RawMaterialInventoryDetailView.as_view(), name='raw_material_inventory_detail'),

    path('finished_product_inventory/', FinishedProductInventoryListCreateView.as_view(), name='finished_product_inventory_list_create'),
    path('finished_product_inventory/<int:pk>/', FinishedProductInventoryDetailView.as_view(), name='finished_product_inventory_detail'),

    path('production/', ProductionListCreateView.as_view(), name='production_list_create'),
    path('production/<int:pk>/', ProductionDetailView.as_view(), name='production_detail'),

    path('move_to_production/', MoveToProductionAPIView.as_view(), name='move_to_production'),
    path('move_to_finished_goods/', MoveToFinishedGoodsAPIView.as_view(), name='move_to_finished_goods'),
    path('return_to_raw_materials/', ReturnToRawMaterialsAPIView.as_view(), name='return_to_raw_materials'),

    path('movement_log/', MovementLogListCreateView.as_view(), name='movement_log_list_create'),
    path('movement_log/<int:pk>/', MovementLogDetailView.as_view(), name='movement_log_detail'),


    path('find-product/', FindProductByBarcodeAPIView.as_view()),
    path('barcoded-products/', BarcodedProductListAPIView.as_view()),
    path('barcode-categories/', BarcodeCategoryListAPIView.as_view(),),
    path('register-product/', RegisterBarcodedProductAPIView.as_view(), name='register-product'),
]
