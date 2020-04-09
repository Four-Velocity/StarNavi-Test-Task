from django.db.models.signals import post_save, pre_delete, m2m_changed, pre_save
from django.dispatch import receiver
import os
from star_navi_backend.utils import generate_adorable_avatar
from .models import User, Post, Like, UserProfile
from PIL import Image

@receiver(post_save, sender=User)
def avatar_work(sender, instance=None, created=False, **kwargs):
    """
    Generate avatar for new user
    """
    if created:
        avatar = generate_adorable_avatar(instance.username)
        UserProfile.objects.create(owner=instance, avatar=avatar)
    if not created and instance.is_active:
        try:
            profile = UserProfile.objects.get(owner=instance)
        except UserProfile.DoesNotExist:
            profile = None
        if profile is None:
            avatar = generate_adorable_avatar(instance.username)
            UserProfile.objects.create(owner=instance, avatar=avatar)


@receiver(post_save, sender=UserProfile)
def avatr_normalize(sender, instance=None, **kwargs):
    """Rename and crop avatar if necessary"""
    avatar = instance.avatar.path
    username = instance.owner.username
    temp = os.path.split(avatar)
    avatar_path = temp[0]
    avatar_ext = os.path.splitext(temp[1])[-1]
    avatar_name = os.path.splitext(temp[1])[0]
    if avatar_name != username:
        for _, _, files in os.walk(avatar_path):
            #Todo: binary search
            for file in files:
                if os.path.splitext(file)[0] == username:
                    os.remove(os.path.join(avatar_path, file))
        new_avatar = os.path.join(avatar_path, username + avatar_ext)
        os.rename(avatar, new_avatar)
        im = Image.open(new_avatar)
        im_w, im_h = im.size
        if im_w != im_h:
            im_min = min(im.size)
            im = im.crop(((im_w - im_min) // 2,
                          (im_h - im_min) // 2,
                          (im_w + im_min) // 2,
                          (im_h + im_min) // 2))
            im.save(new_avatar, quality=100)
        instance.avatar = new_avatar
        instance.save()


@receiver(pre_delete, sender=UserProfile)
def freeze_user(sender, instance=None, **kwargs):
    """Deactivate user on profile delete"""
    user = instance.user
    user.is_active = False
    user.save()
    try:
        avatar = instance.avatar.path
        os.remove(avatar)
    except (ValueError, FileNotFoundError) as e:
        pass


@receiver(post_save, sender=Post)
def post_create(sender, instance=None, created=False, **kwargs):
    """Create Like object, if Post created, normalize image name"""
    if created:
        Like.objects.create(post=instance)
    try:
        image = instance.image.path
        pk = str(instance.pk)
        temp = os.path.split(image)
        image_path = temp[0]
        image_ext = os.path.splitext(temp[1])[-1]
        image_name = os.path.splitext(temp[1])[0]
        if image_name != pk:
            for _, _, files in os.walk(image_path):
                #Todo: binary search
                for file in files:
                    if os.path.splitext(file)[0] == pk:
                        os.remove(os.path.join(image_path, file))
            new_image = os.path.join(image_path, pk + image_ext)
            os.rename(image, new_image)
            instance.image = new_image
            instance.save()
    except ValueError:
        pass


@receiver(m2m_changed, sender=Like.user.through)
def update_likes(sender, instance, **kwargs):
    """Count post's likes"""
    count = instance.user.all().count()
    post = instance.post
    post.likes = count
    post.save()


@receiver(pre_delete, sender=Post)
def image_delete(sender, instance, **kwargs):
    """Delete image when on post delete"""
    try:
        image = instance.image.path
        os.remove(image)
    except (ValueError, FileNotFoundError) as e:
        pass
