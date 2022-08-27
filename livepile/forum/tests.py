from django.test import TestCase
from .model_factories import *
from .forms import *
from django.urls import reverse

# Create your tests here.
class UserTest(TestCase):
    user = None

    def setUp(self):
        self.user = UserFactory.create(username='username', password='password')

    def tearDown(self):
        User.objects.all().delete()

    def test_UserCreated(self):
        created = User.objects.get(pk = self.user.pk)
        self.assertTrue(created)

    def test_UserData(self):
        self.assertEqual(self.user.username, 'username')
        self.assertEqual(self.user.password, 'password')
        self.assertEqual(self.user.email, 'username@example.com')

class ProfileTest(TestCase):
    user = None
    profile = None # prerequisite

    def setUp(self):
        self.user = UserFactory.create(username='username', password='password')
        self.profile = ProfileFactory.create(user=self.user, fname='first', lname='last')
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_ProfileCreated(self):
        created = Profile.objects.get(pk = self.profile.pk)
        self.assertTrue(created)

    def test_ProfileData(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.fname, 'first')
        self.assertEqual(self.profile.lname, 'last')

class TagTest(TestCase):
    tag = None

    def setUp(self):
        self.tag = TagFactory.create(tag='tag')

    def tearDown(self):
        Tag.objects.all().delete()

    def test_TagCreated(self):
        created = Tag.objects.get(pk = self.tag.pk)
        self.assertTrue(created)
    
    def test_TagData(self):
        self.assertEqual(self.tag.tag, 'tag')

class PostTest(TestCase):
    user = None # prerequisite
    author = None # prerequisite
    tag = None # prerequisite
    post_with_tags = None
    post_without_tags = None

    def setUp(self):
        self.user = UserFactory.create(username='username', password='password')
        self.author = ProfileFactory.create(user=self.user, fname='first', lname='last')
        self.tag = TagFactory.create(tag='tag')

        self.post_with_tags = PostFactory.create(title='title', content='content', code='code', author=self.author)
        self.post_with_tags.tags.set([self.tag.pk])

        self.post_without_tags = PostFactory.create(title='title', content='content', code='code', author=self.author)

    def tearDown(self):
        User.objects.all().delete()
    
    def test_PostWithTagsCreated(self):
        created = Post.objects.get(pk = self.post_with_tags.pk)
        self.assertTrue(created)
    
    def test_PostWithoutTagsCreated(self):
        created = Post.objects.get(pk = self.post_without_tags.pk)
        self.assertTrue(created)
    
    def test_PostWithTagsData(self):        
        self.assertEqual(self.post_with_tags.title, 'title')
        self.assertEqual(self.post_with_tags.content, 'content')
        self.assertEqual(self.post_with_tags.code, 'code')
        self.assertEqual(self.post_with_tags.author, self.author)
        for tag in self.post_with_tags.tags.all():
            self.assertEqual(tag, self.tag)

    def test_NumberOfTags(self):
        self.assertEqual(self.post_with_tags.tags.count(), 1)
        self.assertEqual(self.post_without_tags.tags.count(), 0)

class ReplyTest(TestCase):
    user = None # prerequisite
    author = None # prerequisite
    post = None # prerequisite
    reply = None

    def setUp(self):
        self.user = UserFactory.create(username='username', password='password')
        self.author = ProfileFactory.create(user=self.user, fname='first', lname='last')
        self.post = PostFactory.create(title='title', content='content', code='code', author=self.author)
        self.reply = ReplyFactory.create(content='content', code='code', post=self.post, author=self.author)

    def tearDown(self):
        User.objects.all().delete()

    def test_ReplyCreated(self):
        created = Reply.objects.get(pk = self.reply.pk)
        self.assertTrue(created)

    def test_ReplyData(self):
        self.assertEqual(self.reply.content, 'content')
        self.assertEqual(self.reply.code, 'code')
        self.assertEqual(self.reply.post, self.post)
        self.assertEqual(self.reply.author, self.author)

class UserFormTest(TestCase):
    good = None
    bad = None
    invalid = None

    def setUp(self):
        self.good = UserForm(data={'username': 'username', 'email': 'email@example.com', 'password': 'password', 'reenter': 'password'})
        self.invalid = UserForm(data={'username': 'username', 'email': 'email', 'password': 'password'})
        self.bad = UserForm(data={})

    def tearDown(self):
        User.objects.all().delete()

    def test_GoodUserForm(self):
        self.assertTrue(self.good.is_valid())
        self.assertEqual(self.good.errors, {})
    
    def test_BadUserForm(self):
        self.assertFalse(self.bad.is_valid())

    def test_InvalidUserForm(self):
        self.assertEqual(self.invalid.errors['email'], ['Enter a valid email address.'])
        self.assertEqual(self.invalid.errors['reenter'], ['This field is required.'])

class ProfileFormTest(TestCase):
    good = None
    bad = None

    def setUp(self):
        self.good = ProfileForm(data={'fname': 'fname', 'lname': 'lname'})
        self.bad = ProfileForm(data={})

    def tearDown(self):
        Profile.objects.all().delete()

    def test_GoodProfileForm(self):
        self.assertTrue(self.good.is_valid())
        self.assertEqual(self.good.errors, {})
    
    def test_BadProfileForm(self):
        self.assertFalse(self.bad.is_valid())

class UpdateUserFormTest(TestCase):
    good = None
    bad = None
    invalid = None

    def setUp(self):
        self.good = UpdateUserForm(data={'username': 'username', 'email': 'email@example.com'})
        self.invalid = UpdateUserForm(data={'username': 'username', 'email': 'email'})
        self.bad = UpdateUserForm(data={})

    def tearDown(self):
        User.objects.all().delete()

    def test_GoodUpdateUserForm(self):
        self.assertTrue(self.good.is_valid())
        self.assertEqual(self.good.errors, {})
    
    def test_BadUpdateUserForm(self):
        self.assertFalse(self.bad.is_valid())

    def test_InvalidUpdateUserForm(self):
        self.assertEqual(self.invalid.errors['email'], ['Enter a valid email address.'])

class UpdateProfileFormTest(TestCase):
    good = None
    bad = None

    def setUp(self):
        self.good = UpdateProfileForm(data={'fname': 'fname', 'lname': 'lname', 'avatar': 'avatars/default-avatar.png'})
        self.bad = UpdateProfileForm(data={})

    def tearDown(self):
        Profile.objects.all().delete()

    def test_GoodUpdateProfileForm(self):
        self.assertTrue(self.good.is_valid())
        self.assertEqual(self.good.errors, {})
    
    def test_BadUpdateProfileForm(self):
        self.assertFalse(self.bad.is_valid())

class UrlTest(TestCase):
    profile_url = None
    post_url = None
    user = None
    author = None
    post = None

    def setUp(self):
        self.user = UserFactory.create(username='username', password='password')
        self.author = ProfileFactory.create(user=self.user, fname='first', lname='last')
        self.post = PostFactory.create(title='title', content='content', code='code', author=self.author)

        self.profile_url = reverse('profile', args={ self.user })
        self.post_url = reverse('post', args={ self.post.pk })

    def tearDown(self):
        User.objects.all().delete()

    def test_ProfileSuccess(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_PostSuccess(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 200)