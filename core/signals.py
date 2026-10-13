import logging

from django.db import transaction
from django.db.models.signals import post_delete, pre_save

from core.models import Testimonial, HeroImage, SiteSettings
from gallery.models import Photo
from news.models import Notice, Event
from records.models import Student

logger = logging.getLogger(__name__)

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

def get_file_fields(instance):
    """Return the names of file fields on this instance that currently hold a file."""
    field_names = FILE_FIELDS.get(type(instance), [])
    return [name for name in field_names if getattr(instance, name, None)]

def post_delete_cleanup(sender, instance, **kwargs):
    for field_name in get_file_fields(instance):
        field = getattr(instance, field_name, None)
        delete_file(field)

def pre_save_cleanup(sender, instance, **kwargs):
    if kwargs.get('raw'):
        return
    if not instance.pk:
        return
    update_fields = kwargs.get('update_fields')
    file_field_names = FILE_FIELDS.get(sender, [])
    if update_fields is not None and not any(f in update_fields for f in file_field_names):
        return
    try:
        old_instance = sender._default_manager.only(*file_field_names).get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    for field_name in file_field_names:
        old_field = getattr(old_instance, field_name, None)
        new_field = getattr(instance, field_name, None)
        if old_field and old_field.name:
            if not new_field or old_field.name != new_field.name:
                delete_file(old_field)

for model in FILE_FIELDS:
    post_delete.connect(post_delete_cleanup, sender=model,
                        dispatch_uid=f"file_cleanup_delete_{model._meta.label}")
    pre_save.connect(pre_save_cleanup, sender=model,
                     dispatch_uid=f"file_cleanup_save_{model._meta.label}")
