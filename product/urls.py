from django.urls import path, include
from . import views

user_urls = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='getUserProfile'),
    path('register/', views.userRegister, name='userRegister'),
]
order_urls = [
    path('add/', views.addOrder, name='addOrder'),
    path('myorders/', views.getOrders, name='getOrders'),
    path('<int:id_>/', views.orderId, name='getOrderId'),
]
urlpatterns = [
    path('products/', views.get_products, name='products'),
    path('product/<int:id_>', views.get_product, name='product'),
    path('user/', include(user_urls)),
    path('order/', include(order_urls)),
]
