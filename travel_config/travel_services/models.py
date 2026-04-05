from django.db import models

class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    # type hint to resolve IDE warnings
    places: models.Manager['Place']

    @property
    def is_completed(self):
        if not self.places.exists():
            return False
        return not self.places.filter(is_visited=False).exists()


class Place(models.Model):
    project = models.ForeignKey(
        TravelProject,
        related_name='places',
        on_delete=models.CASCADE
    )
    external_id = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'external_id'],
                name='unique_project_external_id'
            )
        ]