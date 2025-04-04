from django.db import models


class BaseModel(models.Model):
    """
    Adjust Django's Model to have default fields like
    created_at and updated_at
    Make default ordering by created_at in descending order
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
