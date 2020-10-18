from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import YoutubeClip, VIP
from app.business import check_VIP_mention 

@receiver(post_save, sender=VIP)
def VIP_update(sender, instance, created,  **kwargs):
    """Calculate mention after updating VIP"""
    if not created:
        # recheck mention for this VIP
        for clip in YoutubeClip.objects.filter(bad_content_status=0):
            clip.check_VIP_mention(level=1, vip=instance)

        for clip in YoutubeClip.objects.filter(bad_content_status__gt=1):
            clip.check_VIP_mention(level=2, vip=instance)
                
           
    