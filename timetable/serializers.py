from rest_framework import serializers as sz

from .models import Timetable, Course, CourseMaterials


class TimetableSerializer(sz.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'
    course = sz.StringRelatedField()
    weekday = sz.StringRelatedField()
    start_time = sz.StringRelatedField()


class TimetableGroupedSerializer(sz.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ('first', 'second')
    first = sz.SerializerMethodField()
    second = sz.SerializerMethodField()

    def get_first(self, instance):
        return TimetableSerializer(instance.weekday.filter(weekday=1, start_time=1), many=True).data

    def get_second(self, instance):
        return TimetableSerializer(instance.weekday.filter(weekday=1, start_time=2), many=True).data


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
