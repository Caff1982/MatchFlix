from rest_framework import serializers
from shows.models import Show


class RecommenderSerealizers(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('title', 'release_year', 'description',
                  'category_string', 'country_string', 'id')