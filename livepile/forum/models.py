from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=255, blank=True)
    lname = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(default='avatars/default-avatar.png', upload_to='avatars/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_num_posts(self):
        return self.posts.all().count()

    def get_posts(self):
        return self.posts.all()

    def get_num_replies(self):
        return self.replies.all().count()

    def get_replies(self):
        return self.replies.all()
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100:
            height = 100
            width = img.width * (img.height / height)
            output_size = (width, height)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tag}"

    class Meta:
        ordering = ('tag',)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    code = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, default=None, related_name='posts')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:70]}"
    
    def get_tags(self):
        return self.tags.all()

    def get_replies(self):
        return self.replies.all()

    def get_num_replies(self):
        return self.replies.all().count()

    def get_elapsed_time(self):
        duration = (datetime.now(timezone.utc) - self.created).total_seconds()
        years = divmod(duration, 32140800)
        months = divmod(years[1], 2678400)
        days = divmod(months[1], 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)

        elapsed = ""
        if (years[0] > 0):
            if (years[0] < 2):
                elapsed = str(int(years[0])) + " year "
            else:
                elapsed = str(int(years[0])) + " years "
        elif (months[0] > 0):
            if (months[0] < 2):
                elapsed = str(int(months[0])) + " month "
            else:
                elapsed = str(int(months[0])) + " months "
        elif (days[0] > 0):
            if (days[0] < 2):
                elapsed = str(int(days[0])) + " day "
            else:
                elapsed = str(int(days[0])) + " days "
        elif (hours[0] > 0):
            if (hours[0] < 2):
                elapsed = str(int(hours[0])) + " hour "
            else:
                elapsed = str(int(hours[0])) + " hours "
        elif (minutes[0] > 0):
            if (minutes[0] < 2):
                elapsed = str(int(minutes[0])) + " min "
            else:
                elapsed = str(int(minutes[0])) + " mins "
        else:
            elapsed = "a while "

        return f"{elapsed}"

    class Meta:
        ordering = ('-created',)

class Reply(models.Model):
    content = models.TextField()
    code = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} replied to '{self.post.title}'"

    def get_elapsed_time(self):
        duration = (datetime.now(timezone.utc) - self.created).total_seconds()
        years = divmod(duration, 32140800)
        months = divmod(years[1], 2678400)
        days = divmod(months[1], 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)

        elapsed = ""
        if (years[0] > 0):
            if (years[0] < 2):
                elapsed = str(int(years[0])) + " year "
            else:
                elapsed = str(int(years[0])) + " years "
        elif (months[0] > 0):
            if (months[0] < 2):
                elapsed = str(int(months[0])) + " month "
            else:
                elapsed = str(int(months[0])) + " months "
        elif (days[0] > 0):
            if (days[0] < 2):
                elapsed = str(int(days[0])) + " day "
            else:
                elapsed = str(int(days[0])) + " days "
        elif (hours[0] > 0):
            if (hours[0] < 2):
                elapsed = str(int(hours[0])) + " hour "
            else:
                elapsed = str(int(hours[0])) + " hours "
        elif (minutes[0] > 0):
            if (minutes[0] < 2):
                elapsed = str(int(minutes[0])) + " min "
            else:
                elapsed = str(int(minutes[0])) + " mins "
        else:
            elapsed = "a while "

        return f"{elapsed}"

    class Meta:
        ordering = ('-created',)