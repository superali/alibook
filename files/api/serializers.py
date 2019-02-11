from django.urls import reverse_lazy
from rest_framework import serializers

from files.models import Picture
class PictureDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields=[
            'created_at',
            'image',

        ]
