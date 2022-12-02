from rest_framework import serializers as sz

from .models import News


class NewsSerializer(sz.ModelSerializer):
    owner = sz.HiddenField(default=sz.CurrentUserDefault())

    class Meta:
        model = News
        fields = '__all__'
