from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Product, Contractor
from .serializers import ProductSerializer, ContractorSerializer
from .pagination import CustomPagination
from .authentication import TokenAuthentication


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title', 'description']

    def get_queryset(self):
        queryset = Product.objects.all()
        order = self.request.query_params.get('order')
        if order:
            queryset = queryset.order_by(order)
        return queryset

    def create(self, request, *args, **kwargs):
        result = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        pk = result.data['id']
        created_product = Product.objects.filter(pk=pk).first()
        if created_product:
            pass
            # TODO Вставить код регистрации в журнале
        return result

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        updated_product = Product.objects.filter(pk=pk).first()
        result = viewsets.ModelViewSet.update(self, request, *args, **kwargs)
        if updated_product:
            updated_product.refresh_from_db()
            # TODO Вставить код регистрации в журнале
        return result


class ContractorViewSet(viewsets.ModelViewSet):
    serializer_class = ContractorSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title']

    def get_queryset(self):
        queryset = Contractor.objects.all()
        order = self.request.query_params.get('order')
        if order:
            queryset = queryset.order_by(order)
        return queryset


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contractor_categories(request):
    data = {machine_name: human_name for machine_name, human_name in Contractor.CONTRACTOR_CATEGORY}
    return Response(data)
