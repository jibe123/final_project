import secrets

from rest_framework import serializers

from .models import User, Student, Group


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)

    class Meta:
        model = Group
        fields = '__all__'


class GroupField(serializers.RelatedField):
    def get_queryset(self):
        return Group.objects.all()

    def to_internal_value(self, data):
        try:
            return Group.objects.get(id=data)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Такой группы не существует!')
        except ValueError:
            raise serializers.ValidationError('Введите id группы!')

    def to_representation(self, value):
        return GroupSerializer(value).data


class CreateStudentSerializer(serializers.ModelSerializer):
    auto_password = serializers.HiddenField(default=True)
    is_student = serializers.BooleanField(default=True)
    password = serializers.CharField(write_only=True, default="")
    group = GroupField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'auto_password', 'is_student', 'password', 'group')
        extra_kwargs = {"first_name": {"required": True},
                        "last_name": {"required": True},
                        "email": {"required": True},
                        "group": {"required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=validated_data.get("email"),
            username="temporary_username",
            auto_password=validated_data.get("auto_password"),
            is_student=validated_data.get("is_student")
        )
        allowed_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        length = 11
        password = "".join(secrets.choice(allowed_chars) for i in range(length))
        user.set_password(password)
        user.check_password(password)
        user.save()
        Student.objects.create(
            user_id=user.id,
            group_id=validated_data.get("group").id)

        return validated_data

    def validate(self, data):
        fields = ['first_name', 'last_name', 'email']
        for field in fields:
            if data[field] is None or len(data[field]) < 2:
                raise serializers.ValidationError
            if 'group' is None:
                raise serializers.ValidationError
        return data
