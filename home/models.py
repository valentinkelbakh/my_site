from time import timezone
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class Entry(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='img', null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self, *args, **kwargs):
        self.published_date = timezone.now()
        return super().save(self, *args, **kwargs)

    def __str__(self):
        return f'{str(self.created_date)[:10]}, {self.author}: {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def TopicNumber(self):
        topics = Topic.objects.filter(category=self)
        return len(topics)

    def __str__(self):
        return self.name


class Topic (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def CommentNumber(self):
        comments = Comment.objects.filter(topic=self)
        return len(comments)
    def __str__(self):
        return f'{self.category.name}: {self.name}'


class Comment (models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{str(self.date)[:10]}, {self.topic.name}, {self.author}:{self.text[:40]}..'


class Booking (models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=12, unique=True)
    date = models.DateTimeField(default=timezone.now)

    class Instrument(models.IntegerChoices):
        GUITAR = 1, "Guitar"
        KEYS = 2, 'Synthesizer'
        ACCORDION = 3, "Piano Accordion"
        BAYAN = 4, 'Chromatic Button Accordion'
        BALALAIKA = 5, 'Balalaika'
    instrument = models.PositiveSmallIntegerField(
        choices=Instrument.choices,
        default=Instrument.GUITAR)

    def __str__(self):
        return f'{self.name}, {self.number}: {self.get_instrument_display()}'
