from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction

from news.models import Notice, Event
from gallery.models import Photo
from records.models import Student
from core.models import Testimonial, HeroImage, SiteSettings

def delete_file(field):
    if field and field.name:
        def do_delete():
            try:
                field.delete(save=False)
            except:
                pass
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

for model_cls, fields in FILE_FIELDS.items():
    def make_post_delete(model, flds):
        @receiver(post_delete, sender=model, dispatch_uid=f"delete_file_post_delete_{model.__name__}")
        def handler(sender, instance, **kwargs):
            for field_name in flds:
                field = getattr(instance, field_name, None)
                delete_file(field)
    make_post_delete(model_cls, fields)

    def make_pre_save(model, flds):
        @receiver(pre_save, sender=model, dispatch_uid=f"delete_file_pre_save_{model.__name__}")
        def handler(sender, instance, **kwargs):
            if not instance.pk:
                return
            try:
                old_instance = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            for field_name in flds:
                old_field = getattr(old_instance, field_name, None)
                new_field = getattr(instance, field_name, None)
                if old_field and old_field.name:
                    if not new_field or old_field.name != new_field.name:
                        delete_file(old_field)
    make_pre_save(model_cls, fields)
