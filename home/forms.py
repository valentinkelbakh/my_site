from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Entry, Comment,Booking,Topic

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'text', 'photo')


class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
        raise forms.ValidationError(f'Username "{username}" is already in use.')

class BookLessonForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("name", "number", "instrument")


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


