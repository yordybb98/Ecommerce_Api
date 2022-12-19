from rest_framework import viewsets

from apps.products.api.serializers.general_serializers import *


class MeasureUnitViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state=True)


class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicadorSerializer
    queryset = IndicadorSerializer.Meta.model.objects.filter(state=True)


class CategoryProductViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryProductSerializer
    queryset = CategoryProductSerializer.Meta.model.objects.filter(state=True)
