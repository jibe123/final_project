from rest_framework import serializers as sz

from .models import Timetable, Course, CourseMaterials


class TimetableSerializer(sz.ModelSerializer):
    course = sz.StringRelatedField(read_only=True)
    weekday = sz.StringRelatedField(read_only=True)
    start_time = sz.StringRelatedField(read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'


class CourseSerializer(sz.ModelSerializer):
    materials = sz.SerializerMethodField()

    def get_materials(self, obj):
        materials = CourseMaterials.objects.filter(course=obj)
        return CourseMaterialsSerializer(
            materials, many=True, read_only=True).data

    class Meta:
        model = Course
        fields = ('id', 'title', 'duration', 'teacher',
                  'groups', 'materials')


class CourseMaterialsSerializer(sz.ModelSerializer):
    class Meta:
        model = CourseMaterials
        fields = '__all__'
