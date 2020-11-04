from rest_framework import serializers
from .models import Show


class ShowSerealizers(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('title', 'release_year', 'description',
                  'category_string', 'country_string')