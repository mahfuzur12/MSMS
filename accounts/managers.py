from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    
    def create_superuser(self, email, password, **kwargs):
        if not kwargs.get("is_superuser"):
            kwargs["is_superuser"] = True
            
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Not possible to create super user')

        kwargs["is_staff"] = True
        kwargs["role"] = "siteadmin"
        return self._create_user(email, password, **kwargs)
    
    
    def create_user(self, email, password=None, **kwargs):
        if not kwargs.get("is_superuser"):
            kwargs["is_superuser"] = True
            
        return self._create_user(email, password, **kwargs)
    

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email is None')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    