from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not phone:
            raise ValueError("Phone number is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        user = self.create_user(email, username, phone, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

USER_ROLES = (
    ('admin', 'admin'),
    ('employee', 'employee'),
    ('cluster', 'cluster'),
)

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
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
    REQUIRED_FIELDS = ['username', 'phone']

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

class Clusteraera(models.Model):
    cluster_aera = models.CharField(max_length=255, null=True,blank=True,default='')
    class Meta:
        managed = True
        db_table = 'cluster_aera'

shop_type = (
        ('panshop', 'pan shop'),
        ('teashop', 'tea shop'),
        ('hosptial','hosptial'),
        ('restrant','restrant'),
    )
class ShopOwner(models.Model):
    shopowner_number = models.CharField(max_length=255,unique=True,default='')
    user = models.ForeignKey('Users', models.DO_NOTHING, null=False,blank=False,related_name='created_user',db_column='users_id')
    shop_name = models.CharField(max_length=255)
    shop_type = models.CharField(choices=shop_type,max_length=100,null=True,blank=True,default='')
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    points = models.DecimalField(max_digits=10, decimal_places=2,default='0')
    rcb_agreed = models.BooleanField(default=True)
    cluser_aera = models.ForeignKey('Clusteraera', models.DO_NOTHING,null=False,blank=False,related_name='cluster',db_column='cluster_aera')
    created_by = models.ForeignKey('Users', models.DO_NOTHING, null=False,blank=False,related_name='created_owner',db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shopowner_number} {self.shop_name}"
    class Meta:
        managed = True
        db_table = 'owner_details'



class WasteType(models.Model):
    wastename = models.CharField(max_length=255)
    image = models.ImageField(upload_to='waste_images/', blank=True, null=True)
    quantity = models.CharField(max_length=255,default="kg")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, null=False,blank=False,related_name='waste_type',db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wastename}"
    class Meta:
        managed = True
        db_table = 'waste_type'


class PickupTransaction(models.Model):
    shop_owner = models.ForeignKey('ShopOwner', models.DO_NOTHING, null=False,blank=False,db_column='shop_owner_id')
    given_bags = models.BooleanField(default=True)
    lifted_status = models.BooleanField(default=True)
    pickup_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    transaction_amount = models.DecimalField(max_digits=10,default= 0.0, decimal_places=2,null=True,blank=True)
    paid_amount = models.DecimalField(max_digits=10, default=0.0 ,decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cluser_aera = models.ForeignKey('Clusteraera', models.DO_NOTHING, null=False,blank=False,related_name='cluster_transaction',db_column='cluster_aera')
    created_by = models.ForeignKey('Users', models.DO_NOTHING, null=False,blank=False,related_name='created_waste_type',db_column='created_by')

    class Meta:
        managed = True
        db_table = 'pickup_transaction'

class PickupWastData(models.Model):
    waste_type = models.ForeignKey('WasteType', models.DO_NOTHING, null=False,blank=False,db_column='waste_type_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=255)
    pickup_transaction = models.ForeignKey('PickupTransaction', models.DO_NOTHING, null=False,blank=False,db_column='pickup_transaction_id')
    
    class Meta:
        managed = True
        db_table = 'pickup_waste_data'

