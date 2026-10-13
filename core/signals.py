from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

from news.models import Notice, Event
from gallery.models import Photo
from records.models import Student
from core.models import Testimonial, HeroImage, SiteSettings

def delete_file(field):
    if field and field.name:
        def do_delete():
            try:
                field.delete(save=False)
            except OSError:
                logger.warning("Failed to delete file.", exc_info=True)
        transaction.on_commit(do_delete)

FILE_FIELDS = {
    Notice: ['file_attachment'],
    Event: ['file_attachment'],
    Photo: ['image'],
    Student: ['photo'],
    Testimonial: ['photo'],
    HeroImage: ['image'],
    SiteSettings: ['logo', 'favicon', 'about_image', 'principal_photo', 'og_image'],
}

@receiver(post_delete)
def post_delete_cleanup(sender, instance, **kwargs):
    if sender in FILE_FIELDS:
        for field_name in FILE_FIELDS[sender]:
            field = getattr(instance, field_name, None)
            delete_file(field)

@receiver(pre_save)
def pre_save_cleanup(sender, instance, **kwargs):
    if sender in FILE_FIELDS:
        if not instance.pk:
            return
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        for field_name in FILE_FIELDS[sender]:
            old_field = getattr(old_instance, field_name, None)
            new_field = getattr(instance, field_name, None)
            if old_field and old_field.name:
                if not new_field or old_field.name != new_field.name:
                    delete_file(old_field)
