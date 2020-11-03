from rest_framework import serializers
from .models import Show


class ShowSerealizers(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('title', 'description')