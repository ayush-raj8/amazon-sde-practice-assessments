from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=120)
    campus = models.CharField(max_length=80)
    category = models.CharField(max_length=80)
    member_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name
