from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.reverse import reverse

from backend.models import Portal, Comment, Tag, TagType


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TagTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = TagType
        fields = ('id', 'url', 'name')

    def get_url(self, obj):
        request = self.context['request']
        return reverse('tagtype-detail', kwargs={'pk': obj.pk}, request=request)


class TagSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()

    up = serializers.HyperlinkedRelatedField(view_name='tag-detail', read_only=True)
    type = TagTypeSerializer()

    class Meta:
        model = Tag
        fields = ('id', 'url', 'name', 'type', 'up')

    def get_url(self, obj):
        request = self.context['request']
        return reverse('tag-detail', kwargs={'pk': obj.pk}, request=request)


class PortalSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()

    # tags = serializers.HyperlinkedRelatedField(view_name='tag-detail',
    #                                            many=True, queryset=Tag.objects.all())

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Portal
        fields = ('id', 'url', 'title', 'link', 'nickname', 'tags')

    def get_url(self, obj):
        request = self.context['request']
        return reverse('portal-detail', kwargs={'pk': obj.pk}, request=request)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()

    portal = serializers.HyperlinkedRelatedField(
        view_name='portal-detail',
        queryset=Portal.objects.all(),
        allow_null=False,
        required=True
    )

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'url', 'body', 'author', 'portal')

    def get_url(self, obj):
        request = self.context['request']
        return reverse('comment-detail', kwargs={'pk': obj.pk}, request=request)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    # article_set = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True, many=True)
    # course_set = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')

    def get_url(self, obj):
        request = self.context['request']
        return reverse('user-detail', kwargs={'pk': obj.pk}, request=request)
