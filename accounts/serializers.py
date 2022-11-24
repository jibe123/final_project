import secrets

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Student, Officer, Group, Department


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class NewUserSerializer(serializers.ModelSerializer):
    user_must_change_password = serializers.HiddenField(default=True)
    is_management = serializers.BooleanField(default=False)
    is_officer = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True, default="")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_must_change_password',
                  'is_management', 'is_officer', 'is_teacher', 'is_student',
                  'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            username="temporary_username",
            user_must_change_password=validated_data.get("user_must_change_password"),
            is_management=validated_data.get("is_management"),
            is_officer=validated_data.get("is_officer"),
            is_teacher=validated_data.get("is_teacher"),
            is_student=validated_data.get("is_student")
        )
        allowed_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        length = 11
        password = "".join(secrets.choice(allowed_chars) for i in range(length))
        user.set_password(password)
        user.check_password(password)
        user.save()

        return user


class GroupField(serializers.RelatedField):
    def get_queryset(self):
        return Group.objects.all()

    def to_internal_value(self, data):
        try:
            try:
                return Group.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'Введите правильный id группы!'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id группы должен быть целым числом!'
                )
        except Group.DoesNotExist:
            raise serializers.ValidationError(
                'Такой группы не существует!'
            )

    def to_representation(self, value):
        return GroupSerializer(value).data


class StudentSerializer(serializers.Serializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.filter(is_student=True))
    group = GroupField()

    class Meta:
        model = Student
        fields = ('user_id', 'group_id',)


class DepartmentField(serializers.RelatedField):
    def get_queryset(self):
        return Department.objects.all()

    def to_internal_value(self, data):
        try:
            try:
                return Department.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'Введите правильный id направления!'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id направления должен быть целым числом!'
                )
        except Department.DoesNotExist:
            raise serializers.ValidationError(
                'Такого направления не существует!'
            )

    def to_representation(self, value):
        return DepartmentSerializer(value).data


class OfficerSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_officer=True))
    department = DepartmentField()

    class Meta:
        model = Officer
        fields = ('user_id', 'department_id',)


class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Department
        fields = '__all__'


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    department = DepartmentField()

    class Meta:
        model = Group
        fields = ('user_id', 'department_id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
