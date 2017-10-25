import datetime

from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from backend import serializers
from backend.permissions import IsOwnerOrReadOnly
from backend.models import Tag, Portal, Comment, Key


EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class DefaultMixin(object):
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
        authentication.TokenAuthentication
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_by = 25
    pagination_by_param = 'page_size'
    max_pagination_by = 100


class IsOwnerOrReadOnlyMixin(DefaultMixin):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )


class ObtainExpiringAuthToken(ObtainAuthToken):
    """Create user token"""

    @csrf_exempt
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

            time_now = timezone.now()

            if created or token.created < (time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)):
                # Update the created time of the token to keep it valid
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = time_now
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params.get('query') == 'myself':  # 查询自己
            user = get_object_or_404(User.objects.all(), pk=request.user.id)
            serializer = serializers.UserSerializer(user)
            serializer.context['request'] = request  # 生成超链接需要
            return Response(serializer.data)
        return super(UserViewSet, self).list(request, args, kwargs)

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = serializers.UserSerializer(user)
    #     serializer.context['request'] = request
    #     return Response(serializer.data)


class GroupViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class PortalViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Portal.objects.all()
    serializer_class = serializers.PortalSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AreaViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class CommentViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IITCView(APIView):

    @csrf_exempt
    def get(self, request, format=None):
        print(self.request.user)
        return Response({})

    @csrf_exempt
    def post(self, request):
        print(self.request.data)
        return Response({})
