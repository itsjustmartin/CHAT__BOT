from django.db import models

# Create your models here.

categories = (
    ('hello','hello'),
    ('what', 'what'),
    ('joke','joke'),
    ('details','details'),
    ('human','human'),
)


class response(models.Model):
    mtext = models.CharField(max_length=200,blank=True,null=True)
    category =models.CharField(max_length=20,blank=True, null=True, choices=categories)

    def __str__(self) :
      return self.mtext
