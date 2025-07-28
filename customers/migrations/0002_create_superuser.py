# customers/migrations/0002_create_superuser.py

from django.db import migrations
from django.contrib.auth.models import User

# --- আপনার সুপারইউজারের তথ্য এখানে দিন ---
SUPERUSER_USERNAME = 'shariful'
SUPERUSER_EMAIL = 'si9504460@gmail.com'
SUPERUSER_PASSWORD = 'your_strong_password_here' # <-- একটি শক্তিশালী পাসওয়ার্ড দিন
# ------------------------------------

def create_superuser(apps, schema_editor):
    """
    Creates a superuser if it doesn't already exist.
    """
    if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
        print(f"\nCreating superuser: {SUPERUSER_USERNAME}")
        User.objects.create_superuser(
            username=SUPERUSER_USERNAME,
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD
        )
    else:
        print(f"\nSuperuser '{SUPERUSER_USERNAME}' already exists.")

def remove_superuser(apps, schema_editor):
    """
    (Optional) This function runs if you ever reverse the migration.
    It's good practice to include it.
    """
    try:
        user = User.objects.get(username=SUPERUSER_USERNAME)
        user.delete()
    except User.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'), # <-- আপনার আগের মাইগ্রেশনের উপর নির্ভর করবে
    ]

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]