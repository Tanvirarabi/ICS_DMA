from django.contrib import admin
from django.urls import path

from . import views  # ✅ FIX: needed for dashboard

from .views import (
    OrganizationListCreateAPIView,
    OrganizationDetailAPIView,

    RawMaterialInventoryListCreateView,
    RawMaterialInventoryDetailView,

    FinishedProductInventoryListCreateView,
    FinishedProductInventoryDetailView,

    ProductionListCreateView,
    ProductionDetailView,

    MoveToProductionAPIView,
    MoveToFinishedGoodsAPIView,
    ReturnToRawMaterialsAPIView,

    MovementLogListCreateView,
    MovementLogDetailView,

    FindProductByBarcodeAPIView,
    BarcodedProductListAPIView,
    BarcodeCategoryListAPIView,
    RegisterBarcodedProductAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Dashboard (FIXED)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Organizations
    path('organizations/', OrganizationListCreateAPIView.as_view()),
    path('organizations/<int:pk>/', OrganizationDetailAPIView.as_view()),

    # Raw Materials
    path('raw_material_inventory/', RawMaterialInventoryListCreateView.as_view()),
    path('raw_material_inventory/<int:pk>/', RawMaterialInventoryDetailView.as_view()),

    # Finished Products
    path('finished_product_inventory/', FinishedProductInventoryListCreateView.as_view()),
    path('finished_product_inventory/<int:pk>/', FinishedProductInventoryDetailView.as_view()),

    # Production
    path('production/', ProductionListCreateView.as_view()),
    path('production/<int:pk>/', ProductionDetailView.as_view()),

    # Movement APIs
    path('move_to_production/', MoveToProductionAPIView.as_view()),
    path('move_to_finished_goods/', MoveToFinishedGoodsAPIView.as_view()),
    path('return_to_raw_materials/', ReturnToRawMaterialsAPIView.as_view()),

    # Logs
    path('movement_log/', MovementLogListCreateView.as_view()),
    path('movement_log/<int:pk>/', MovementLogDetailView.as_view()),

    # Barcode system
    path('find-product/', FindProductByBarcodeAPIView.as_view()),
    path('barcoded-products/', BarcodedProductListAPIView.as_view()),
    path('barcode-categories/', BarcodeCategoryListAPIView.as_view()),
    path('register-product/', RegisterBarcodedProductAPIView.as_view(), name='register-product'),
]