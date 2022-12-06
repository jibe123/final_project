from rest_framework import serializers as sz

from .models import (
    Timetable, Course, CourseMaterials)


class TimetableSerializer(sz.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'


class CourseSerializer(sz.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'duration', 'teacher',
                  'groups', 'materials')
    materials = sz.SerializerMethodField()

    def get_materials(self, obj):
        materials = CourseMaterials.objects.filter(course=obj)
        return CourseMaterialsSerializer(
            materials, many=True, read_only=True).data


class CourseMaterialsSerializer(sz.ModelSerializer):
    class Meta:
        model = CourseMaterials
        fields = '__all__'
