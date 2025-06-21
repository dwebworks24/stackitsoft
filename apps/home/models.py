from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

from core import settings

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, phone, employee_id, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not phone:
            raise ValueError("Phone number is required")
        if not employee_id:
            raise ValueError("Employee ID is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            employee_id=employee_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, employee_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, phone, employee_id, password, **extra_fields)


USER_ROLES = (
    ('admin', 'admin'),
    ('employee', 'employee'),
    ('manager', 'manager'),
)

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    employee_id = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    referal_code = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(blank=True, null=True)
    otp_timestamp = models.DateTimeField(default=None, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','employee_id', 'phone']

    objects = UserManager()

    role = models.CharField(choices=USER_ROLES, max_length=100, null=True, blank=True, default='admin')

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# models.py
class MarketCoin(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)

    price_2pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_3pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_4pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_5pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_6pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_7pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_8pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_9pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_10pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_11pm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at =  models.DateTimeField(auto_now=True)
    update_at =   models.DateTimeField(auto_now=True)

    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='market_updates'
    )
    

    def __str__(self):
        return f"{self.name} ({self.unit}) {self.created_at}"