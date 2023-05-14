import random
from django.contrib.auth.models import User,UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,send_mail
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migratons = True
    def _create_user(self,username,phone_number,email,password,is_active,is_staff,is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError("SABT KON")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,email=email,username=username
                          ,is_staff=is_staff,is_superuser=is_superuser,is_active=is_active,date_joined=now, **extra_fields)
        if not extra_fields.get("no_password"):
            user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,username=None,phone_number=None,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        if username is None:
            if not email:
                email = random.choice("abcdefghjklimnopqyxz"+str(phone_number)[-7:])
            if phone_number:
                username = random.choice("abcdefghjklimnopqyxz"+str(phone_number)[-7:])
            while User.objects.filter(username=username).exists():
                username +=str(random.randint(10,99))
        return self._create_user(username,phone_number,email,password,**extra_fields)

    def create_superuser(self,username,phone_number,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username,phone_number,email,password,**extra_fields)
    def get_by_phone_number(self, phone_number):
        return self.get(**{"phone_number":phone_number})
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(_("username"),max_length=32,unique=True,error_messages={"unique":"tekrari"},
                                help_text=_("benvis"),
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z0-9_\.][a-zA-Z]*$',_("enter valid pass"),
                                "invalid")])

    first_name = models.CharField(_("first name"),max_length=30,blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"),unique=True,blank=True,null=True)
    phone_number = models.BigIntegerField(_("phone number"),unique=True,blank=True,null=True,validators=[validators.RegexValidator(r'^989[0-3,9]\d{8}$',_("enter number"))],error_messages={"unique":"tekrari"})
    is_staff = models.BooleanField(_("staff status"),default=False)
    is_active = models.BooleanField(_("active status"), default=False)
    date_joined = models.DateTimeField(_("date joined"),default=timezone.now)
    last_seen = models.DateTimeField(_("last seen"), null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS  = ["email","phone_number"]
    class Meta:
      db_table = "users"
      verbose_name = _("user")
      verbose_name_plural = _("users")




class UserProfile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick_name"),max_length=150,blank=True)
    avatar = models.ImageField(_("avatar"),blank=True)
    birthday = models.DateField(_("birthday"),null=True,blank=True)
    gender =models.BooleanField(_("gender"),help_text="female is false",null=True)
    province = models.ForeignKey(verbose_name=_("province"),to= "Province",null=True,on_delete=models.SET_NULL)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    # phone_number = models.BigIntegerField(_("phone number"), unique=True, blank=True, null=True, validators=[
    #     validators.RegexValidator(r'^989[0-3,9]\d{8}$', ("enter number"), error_messages={"unique": "tekrari"})
    class Meta:
      db_table = "user_profiles"
      verbose_name = _("userprofile")
      verbose_name_plural = _("user_profiles")
class Devices(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES=((WEB,"web"),(IOS,"ios"),(ANDROID,"android"))
    user = models.ForeignKey(User,related_name="devices",on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_("Device uuid"),null=True)
    last_login = models.DateField("Last Login",null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES,default=WEB)
    device_os =models.CharField(_("Device Os "),max_length=20,blank=True)
    device_model = models.CharField(_("Device Model "), max_length=50, blank=True)
    app_version = models.CharField(_("app version"), max_length=20, blank=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    class Meta:
      db_table = "user_devices"
      verbose_name = _("device")
      verbose_name_plural = _("devices")
      unique_together = ("user","device_uuid")

class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


