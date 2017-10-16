from django.test import TestCase

from django.contrib.auth.models import User
from backend.models import Portal, Comment, Area, Key


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='bllli', is_superuser=True)
        self.user2 = User.objects.create(username='test user2')
        self.user3 = User.objects.create(username='test user3')

        self.hb = Area.objects.create(name='华北')
        self.ts = Area.objects.create(name='唐山', up=self.hb)
        self.tsxy = Area.objects.create(name='唐山学院', up=self.ts)
        self.tsxy: Area

        self.portal = Portal.objects.create(title="小青的麒麟",
                                            link='https://ingress.com/intel?ll=39.674865,118.159642'
                                                 '&z=17&pll=39.674865,118.159642',
                                            author=self.user)

        self.tsxy.add_portal(self.portal)

        self.portal.add_keys(user=self.user2, number=999)
        self.portal.add_keys(user=self.user3, number=998)
        self.portal.add_keys(user=self.user3, number=1)

        self.portal.create_comment(user=self.user2, body='哈哈哈哈哈哈')

    def test_models(self):
        self.assertTrue(self.user.username == 'bllli')
        self.hb: Area
        self.assertIn(self.ts, self.hb.area_set.all())
        self.assertIn(self.portal, self.hb.portal_set.all())
        self.assertTrue(len(self.portal.comment_set.all()) > 0)

        self.user3: User
        print(self.user3.key_set.filter(portal=self.portal).all())
