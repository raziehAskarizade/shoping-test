from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Products, Order, OrderItem
from rest_framework import status
from .serializers import ProductsSerializers, UserSerializer, UserSerializerWithToken, OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
def get_products(request):
    products = Products.objects.all()
    serialize_products = ProductsSerializers(products, many=True)
    return Response(serialize_products.data)


@api_view(['GET'])
def get_product(request, id_):
    product = Products.objects.get(id=id_)
    serialize_product = ProductsSerializers(product, many=False)
    return Response(serialize_product.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    user_serializer = UserSerializer(user, many=False)
    return Response(user_serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllUser(request):
    user = User.objects.all()
    return Response(UserSerializer(user, many=True).data)


@api_view(['POST'])
def userRegister(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        user_serializer = UserSerializerWithToken(user, many=False)
        return Response(user_serializer.data)
    except:
        return Response({'detail': 'ایمیل موجود است.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrder(request):
    user = request.user
    data = request.data
    orderItem = data['orderItems']
    if orderItem and len(orderItem) == 0:
        return Response({'detail': 'سفارشی نیست!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            order = Order.objects.get(user=user)
        except:
            order = Order.objects.create(
                user=user,
                total_price=data['total_price'],
            )

    for all_orders in orderItem:
        product = Products.objects.get(id=all_orders['product'])
        if OrderItem.objects.get(title=product.title) != "":
            OrderItem.objects.filter(title=product.title).update(
                quantity=all_orders['quantity'] + OrderItem.objects.get(title=product.title).quantity)
            product.quantity -= all_orders['quantity']
        else:
            item = OrderItem.objects.create(
                product=product,
                order=order,
                title=product.title,
                quantity=all_orders['quantity'],
                price=all_orders['price'],
                image=product.image.url,
            )
            product.quantity -= item.quantity
        product.save()

    return Response(OrderSerializer(order, many=False).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    orders = user.order_set.all()
    orders_serializer = OrderSerializer(orders, many=True)
    return Response(orders_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleterOrderId(request, id_):
    orderItem = OrderItem.objects.get(id=id_)
    quantity = orderItem.quantity
    title = orderItem.title
    Products.objects.filter(title=title).update(quantity=quantity + Products.objects.get(title=title).quantity)
    Products.objects.get(title=title).save()
    OrderItem.objects.get(id=id_).delete()
    return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/api/v1/order/myorders/')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderId(request, id_):
    try:
        user = request.user
        order = Order.objects.get(id=id_)

        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'مجوز صادر نشد'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'سفارش موجود نیست'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getByTime(request, user_id, month, day):
    try:
        user = User.objects.get(id=user_id)
        order = Order.objects.get(created__month=month, created__day=day)
        if order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'دسترسی ندارید'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'سفارشی در این تاریخ ثبت نشده است'}, status=status.HTTP_404_NOT_FOUND)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user, many=False).data
        # for k, v in serializer.items():
        #     data[k] = v

        return serializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
