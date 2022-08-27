from .models import *
import factory

class UserFactory(factory.django.DjangoModelFactory):
    username = 'test'
    password = 'test'
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)

    class Meta:
        model = User

class ProfileFactory(factory.django.DjangoModelFactory):
    fname = 'test'
    lname = 'test'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Profile

class TagFactory(factory.django.DjangoModelFactory):
    tag = 'test'

    class Meta:
        model = Tag

class PostFactory(factory.django.DjangoModelFactory):
    title = 'test'
    content = 'test'
    code = 'test'
    author = factory.SubFactory(ProfileFactory)

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    class Meta:
        model = Post

class ReplyFactory(factory.django.DjangoModelFactory):
    content = 'test'
    code = 'test'
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(ProfileFactory)

    class Meta:
        model = Reply