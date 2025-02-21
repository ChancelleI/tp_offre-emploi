from django.db import models

# Create your models here.


class JobOffer(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.company} ({self.source})"
