from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = '__all__'
