from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile
# Create your models here.
class Project(models.Model):
    ## here .Model Represents that it is officially a class
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
       
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
     # null=True means that we are allowed to submit the for without any description - can be null in the database
     # blank=True whenever we are submitting some kind of or making some post request , we can submit this value with this field being blank - can be empty for django's reference
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    ## Creating many to many relationship as one tag can be given to many models and many models can have many tags
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    ## vote_total amount of times the project has been voted on 
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    ## what percentages of the votes were positive or negative
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    # The __str__ function is used add a string representation of a model's object, so that is
    # to tell Python what to do when we convert a model instance into a string.
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # up is actual value in the data base
    # Up vote is what it shows us
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,blank=True   )
    ## CASCADE - If the project is deleted we delete all the reviews  
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # We have the foreign key here as we need to link which project is this particular review about to store it in the data base
    # on_delete = model.CASCADE deletes our review if the project is deleted

    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
    ## The __str__ method is called when the following functions 
    # are invoked on the object and return a string


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
