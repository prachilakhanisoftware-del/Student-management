from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver

from .models import students


@receiver(post_save, sender=students)
def student_created(sender, instance, created, **kwargs):

    if created:
        print("New student added:", instance.name)
    else:
        print("Student updated")


@receiver(pre_delete, sender=students)
def delete_student_files(sender, instance, **kwargs):

      # Delete student photo
    if instance.photo:
        instance.photo.delete(save=False)

    # Delete all uploaded documents
    for document in instance.documents.all():
        if document.file:
            document.file.delete(save=False)