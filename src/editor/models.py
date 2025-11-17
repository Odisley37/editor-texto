from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255, default="Documento em branco")
    content_html = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
