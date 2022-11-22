from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=100, unique=True, verbose_name="Имя пользователя")
    first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Фамилия")
    email = models.EmailField(
        blank=True, null=True, verbose_name="E-mail")
    is_active = models.BooleanField(
        default=True, verbose_name="Активный пользователь")
    user_must_change_password = models.BooleanField(
        default=False, verbose_name="Пароль должен быть изменен")
    user_image = models.ImageField(
        null=True, blank=True, upload_to="images/", verbose_name="Фото профиля")
    is_management = models.BooleanField(
        default=False, verbose_name="Руководство")
    is_officer = models.BooleanField(
        default=False, verbose_name="Сотрудник")
    is_teacher = models.BooleanField(
        default=False, verbose_name="Преподаватель")
    is_student = models.BooleanField(
        default=False, verbose_name="Студент")

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        is_new = self.id is None
        if self.first_name and self.last_name and is_new:
            self.username = self.make_username(self.first_name, self.last_name)
        super(User, self).save(force_insert, force_update)
        if is_new:
            if self.is_student:
                Student.objects.create(user_id=self.id)
            if self.is_officer:
                Officer.objects.create(user_id=self.id)

    @classmethod
    def make_username(cls, first_name, last_name):
        val = f"{first_name}.{last_name}".lower().replace(' ', '')
        x = 0
        while True:
            if x == 0 and User.objects.filter(username=val).count() == 0:
                return val
            else:
                new_val = f"{val}{x}"
                if User.objects.filter(username=new_val).count() == 0:
                    return new_val
            x += 1

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, **kwargs):
        if not first_name:
            raise ValueError("У пользователя должно быть имя")
        if not last_name:
            raise ValueError("У пользователя должна быть фамилия")

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          user_must_change_password=kwargs.get("user_must_change_password"),
                          username=kwargs.get("username"),
                          is_management=kwargs.get("is_management"),
                          is_officer=kwargs.get("is_officer"),
                          is_teacher=kwargs.get("is_teacher"),
                          is_student=kwargs.get("is_student")
                          )
        user.save(using=self._db)
        return user


class Department(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название направления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"


class Officer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name="Пользователь")
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="officers",
        null=True, verbose_name="Направление")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Group(models.Model):
    name = models.CharField(
        max_length=10, unique=True, verbose_name="Название группы")
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="groups",
        verbose_name="Направление")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name="Пользователь")
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, related_name="students",
        null=True, verbose_name="Группа")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
