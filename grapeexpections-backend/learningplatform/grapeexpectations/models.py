import uuid
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Register(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    workemail = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    # Use Django's built-in password hashing
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    empid = models.BigIntegerField(primary_key=True, unique=True)


    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Profile(models.Model):
    class Vertical(models.TextChoices):
        GTT = 'GTT', _('GTT')
        H_I = 'H&I', _('H&I')
        BANKING = 'Banking', _('Banking')
        FS = 'FS', _('FS')
        OTHERS = 'Others', _('Others')

    profileid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empid = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='profiles')
    role = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    vertical = models.CharField(max_length=10, choices=Vertical.choices)

class ResumeImage(models.Model):
    resumeid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empid = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='resume_images')
    image = models.ImageField(upload_to='resumes/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    answerid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empid = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('empid', 'question')
    