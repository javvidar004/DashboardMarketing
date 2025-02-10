from django.db import models

# Create your models here.
class Countries(models.Model):
    country_id = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'countries'


class Devices(models.Model):
    device_id = models.IntegerField(primary_key=True)
    device_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'devices'

class Entretaiment(models.Model):
    entertainment_id = models.IntegerField(primary_key=True)
    entertainment_name = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'entretaiment'


class Gender(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'gender'


class MediaGoal(models.Model):
    goal_id = models.IntegerField(primary_key=True)
    goal_name = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'media_goal'


class Occupations(models.Model):
    occupation_id = models.IntegerField(primary_key=True)
    occupation_name = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'occupations'


class SocialMedia(models.Model):
    socialm_id = models.IntegerField(primary_key=True)
    socialm_name = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'social_media'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, models.DO_NOTHING)
    country = models.ForeignKey(Countries, models.DO_NOTHING)
    d_sm_time = models.FloatField()
    d_entertain_time = models.FloatField()
    sm_plat_used = models.IntegerField()
    primary_plat = models.ForeignKey(SocialMedia, models.DO_NOTHING)
    d_message_time = models.FloatField()
    d_vid_cont_time = models.FloatField()
    d_gaming_time = models.FloatField()
    occupation = models.ForeignKey(Occupations, models.DO_NOTHING)
    monthly_income = models.FloatField()
    device_sm = models.ForeignKey(Devices, models.DO_NOTHING)
    subscription_plats = models.IntegerField()
    avg_sleep_time = models.FloatField()
    physical_activity_tiem = models.FloatField()
    reading_time = models.FloatField()
    work_study_time = models.FloatField()
    screen_time = models.FloatField()
    d_num_notifications = models.IntegerField()
    d_music_time = models.FloatField()
    preferred_content_id = models.IntegerField()
    primary_sm_goal = models.ForeignKey(MediaGoal, models.DO_NOTHING)
    preferred_enter_plat = models.ForeignKey(SocialMedia, models.DO_NOTHING, related_name='users_preferred_enter_plat_set')
    online_comm_time = models.FloatField()
    news_time = models.FloatField()
    ad_interaction_count = models.IntegerField()
    education_plat_time = models.FloatField()
    tech_savviness_level = models.IntegerField()
    devide_for_entertainment = models.ForeignKey(Devices, models.DO_NOTHING, related_name='users_devide_for_entertainment_set')
    sleep_quality = models.IntegerField()
    monthly_spent_entertain = models.FloatField()

    class Meta:
        managed = False
        db_table = 'users'