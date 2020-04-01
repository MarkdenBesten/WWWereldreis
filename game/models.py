import uuid  # Required for unique ID
from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse

from users.models import User


# Create your models here.
class Question(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nr = models.IntegerField()
    title = models.CharField(max_length=300)
    content = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    # declare the location parameters
    Alat = models.FloatField()
    Alon = models.FloatField()
    Blat = models.FloatField()
    Blon = models.FloatField()
    Clat = models.FloatField()
    Clon = models.FloatField()
    Dlat = models.FloatField()
    Dlon = models.FloatField()

    # Metadata
    class Meta:
        ordering = ['nr']
        permissions = (("can_edit", "Can create, edit or delete questions"),
                       ("can_view_answer", "Can view all answers"),
                       ("can_view_all_questions", "Can view all questions"),
                       )

    # Methods
    @property
    def area(self):
        # long = x, lat = y
        area = (
            ((self.Alon * self.Blat) - (self.Alat * self.Blon)) +
            ((self.Blon * self.Clat) - (self.Clon * self.Blat)) +
            ((self.Clon * self.Dlat) - (self.Dlon * self.Clat)) +
            ((self.Dlon * self.Alat) - (self.Alon * self.Dlat))
        )/2
        return abs(area)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.nr) + ': ' + self.title

    def get_absolute_url(self):
        return reverse('question-detail-view', args=[str(self.id)])


class TeamProfile(models.Model):
    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    jokers = models.IntegerField(default=0)
    timeWrong = models.DateTimeField(default=datetime.now())
    timeJoker = models.DateTimeField(default=(datetime.now() + timedelta(minutes=15)))

    # Metadata

    # Methods
    @property
    def current_question(self):
        """Get the sum of jokers and points to get the current question nr"""
        return self.points + self.jokers + 1

    def __str__(self):
        return str(self.user.username)


class Answer(models.Model):
    # Fields
    time = models.DateTimeField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    longitude = models.FloatField(null=True, default=0)
    latitude = models.FloatField(null=True, default=0)
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE)

    RESULT_STATUS = (
        ('g', 'Goed'),
        ('f', 'Fout'),
        ('j', 'Joker'),
    )

    result = models.CharField(
        max_length=1,
        choices=RESULT_STATUS,
        blank=False,
    )

    # Metadata

    # Methods
    def __str__(self):
        return self.team.user.__str__() + str(self.question.nr) + self.result
