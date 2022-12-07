from rest_framework import serializers

from apps.products.models import *


class MeasureUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasureUnit
        exclude = ('state', 'created_date', 'updated_date', 'deleted_date')


class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProduct
        exclude = ('state', 'created_date', 'updated_date', 'deleted_date')


class IndicadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        exclude = ('state', 'created_date', 'updated_date', 'deleted_date')
