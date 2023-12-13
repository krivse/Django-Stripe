from django.urls import path
from .views import ItemViewSet, BuyViewSet, ItemsViewSet, OrderViewSet


urlpatterns = [
    path('order/', OrderViewSet.as_view({'get': 'list'})),
    path('order/<pk>/', OrderViewSet.as_view({'post': 'create'})),
    path('item/<pk>/', ItemViewSet.as_view({'get': 'retrieve'})),
    path('', ItemsViewSet.as_view({'get': 'list'})),
    path('buy/<slug:pk>/', BuyViewSet.as_view({'get': 'retrieve'}),),

]


