from django.db import models
from django.utils import timezone, html
from django.contrib.auth.models import User


class TagType(models.Model):
    """标签类型"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<TagType: %s>' % self.name


class Tag(models.Model):
    """Portal所处的标签

    如天津/北京/华中等物理区域 如成就/常驻蓝/战略/5分钟肉防
    """
    name = models.CharField(max_length=100)

    up = models.ForeignKey('Tag', null=True, blank=True)
    type = models.ForeignKey(TagType, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag: %s>' % self.name

    def add_portal(self, portal, recursive=False):
        if recursive and self.up:  # 为某个po添加一个位置标签时，同时递归的添加父标签
            self.up.add_portal(portal, recursive)
        self.portal_set.add(portal)


class Portal(models.Model):
    """
    Portal
    """
    guid = models.CharField(max_length=40, null=True)
    late6 = models.CharField(max_length=20, null=True)
    lnge6 = models.CharField(max_length=20, null=True)
    image = models.CharField(max_length=300, null=True)
    timestamp = models.BigIntegerField(null=True)

    title = models.CharField(max_length=1000)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField()

    # 标签集 如一个po可同时添加 “华北”/“唐山”/“唐山市路北区”
    tags = models.ManyToManyField(Tag, related_name='portal_set')
    # 对于未授权用户来说，仅能查看自己手动添加link的portal
    adder = models.ManyToManyField(User, related_name='portal_added_set', blank=True)
    author = models.ForeignKey(User, related_name='portal_created_set')

    keys = models.ManyToManyField(User, through='Key', related_name='portal_key_set')

    class Meta:
        ordering = ('id', 'title', 'link')

    def __str__(self):
        return '%s @ %s' % (self.title, self.link)

    def __repr__(self):
        return '<Portal: %s@%s>' % (self.title, self.link)

    def create_comment(self, user, body):
        self.comment_set.create(body=body, author=user)

    def add_keys(self, user, number=1, force=False):
        key, created = self.key_set.get_or_create(holder=user, defaults={'number': number})
        if not created:
            if force:
                key.number = number
            else:
                key.number += number


class Comment(models.Model):
    """
    对某个Portal的评论
    如：“本Po地处偏僻，建议特工结伴前往” / “Portal处于收费公园内”
    """
    body = models.TextField()

    block = models.BooleanField(default=False)

    portal = models.ForeignKey(Portal)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ('body',)

    def __str__(self):
        return '%s for %s' % (self.body, self.portal)

    def refresh_block(self):
        self.block = not self.block


class Key(models.Model):
    number = models.IntegerField()
    update_date = models.DateTimeField(default=timezone.now)

    portal = models.ForeignKey(Portal)
    holder = models.ForeignKey(User)

    def __str__(self):
        return '%s@%s by %s' % (self.number, self.portal.title, self.holder.username)

    def __repr__(self):
        return '<Key: %s>' % self.__str__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.update_date = timezone.now()
        super(Key, self).save(force_insert=force_insert, force_update=force_update,
                              using=using, update_fields=update_fields)
