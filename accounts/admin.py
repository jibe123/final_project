from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput

from .models import User, Group, Department, Officer, Student

admin.site.register(Group)
admin.site.register(Department)
admin.site.register(Officer)
admin.site.register(Student)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'is_management', 'is_officer', 'is_teacher', 'is_student')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the accounts, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change accounts instances
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on accounts.User.
    list_display = ('username', 'is_management', 'is_officer', 'is_teacher', 'is_student')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password',
                           'is_management', 'is_officer',
                           'is_teacher', 'is_student')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'password1', 'password2',
                       'is_management', 'is_officer', 'is_teacher', 'is_student'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
