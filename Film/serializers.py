from rest_framework import serializers

from Film.models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('title', 'content', 'cat')


