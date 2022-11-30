from rest_framework import serializers

from .models import CourseDay, Course, CourseMaterials


class GroupsUpdateSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    mode = serializers.CharField()


class CourseDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDay
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    def get_materials(self, obj):
        materials = CourseMaterials.objects.filter(course=obj)
        return CourseMaterialsSerializer(materials, many=True, read_only=True).data

    class Meta:
        model = Course
        fields = ('id', 'title', 'duration', 'teacher', 'groups', 'materials')


class CourseMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterials
        fields = '__all__'
