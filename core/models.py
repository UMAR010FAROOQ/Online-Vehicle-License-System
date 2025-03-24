from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone


class ChangePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class LearnerApply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=20)
    citizen_type = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=10)
    nationality = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=3)
    disability = models.CharField(max_length=3)
    category = models.CharField(max_length=20)
    permanent_province = models.CharField(max_length=50)
    permanent_district = models.CharField(max_length=50)
    permanent_address = models.TextField()
    current_province = models.CharField(max_length=50)
    current_district = models.CharField(max_length=50)
    current_address = models.TextField()
    user_profile_img = models.ImageField(upload_to='uploads/backimg/')
    id_front_side = models.ImageField(upload_to='uploads/backimg/')
    id_back_side = models.ImageField(upload_to='uploads/backimg/')

    psid = models.CharField(max_length=8, unique=True, editable=False, default="")
    pystatus = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.psid:
            self.psid = self.generate_unique_psid()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_psid():
        while True:
            psid = str(random.randint(10000000, 99999999))
            if not LearnerApply.objects.filter(psid=psid).exists():
                return psid

    def __str__(self):
        return self.full_name




class LearningMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/learning_materials/')
    icon = models.ImageField(upload_to='uploads/learning_materials/icons/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class FeeStructure(models.Model):
    category = models.CharField(max_length=20)
    testFee = models.CharField(max_length=20)
    afterPassingTest = models.CharField(max_length=20)
    courierFee = models.CharField(max_length=20)
    totalFee = models.CharField(max_length=20)     