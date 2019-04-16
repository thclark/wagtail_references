from rest_framework import serializers
from .models import Reference


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Reference

        fields = (
            'slug',
            'bibtype',
            'bibtex',
            'bibjson'
        )

        read_only_fields = (
            'slug',
            'bibtype',
        )

        depth = 1
