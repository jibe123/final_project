from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, Group, Student

admin.site.register(Group)
admin.site.register(Student)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'is_manager', 'is_teacher', 'is_student')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm

    list_display = ('id', 'username', 'is_manager', 'is_teacher', 'is_student')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_manager',
                           'is_teacher', 'is_student', 'is_active',
                           'auto_password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'password1', 'password2',
                       'is_manager', 'is_teacher', 'is_student',
                       'auto_password', 'email'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
