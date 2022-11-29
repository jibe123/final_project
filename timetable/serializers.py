from rest_framework import serializers

from .models import CourseDay


class GroupsUpdateSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    mode = serializers.CharField()


class CourseDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDay
        fields = '__all__'
