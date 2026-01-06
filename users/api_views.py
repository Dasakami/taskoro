from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CharacterClass
from .serializers import (
    CustomUserCreateSerializer,
    UserSearchSerializer,
    ProfileSerializer,
    CharacterClassSerializer,
)

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    """
    POST /api/users/register/
    Регистрация нового пользователя
    """
    serializer_class = CustomUserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': response.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    POST /api/users/login/
    Авторизация пользователя
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
        })


class LogoutAPIView(APIView):
    """
    POST /api/users/logout/
    Выход с блэклистингом refresh token
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileAPIView(RetrieveAPIView):
    """
    GET /api/users/me/
    Получить полный профиль текущего пользователя
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserProfileByIdAPIView(RetrieveAPIView):
    """
    GET /api/users/profiles/{user_id}/ или /api/users/users/{user_id}/
    Получить профиль пользователя по ID (публичный доступ)
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        from django.shortcuts import get_object_or_404
        user = get_object_or_404(User, pk=user_id)
        return user.profile

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UpdateProfileAPIView(UpdateAPIView):
    """
    PATCH /api/users/me/edit/
    Обновить профиль текущего пользователя
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        
        # Обрабатываем avatar отдельно, если он есть в файлах
        if 'avatar' in request.FILES:
            instance.avatar = request.FILES['avatar']
            instance.save()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UserSearchAPIView(ListAPIView):
    """
    GET /api/users/search/?q=…
    Поиск пользователей по username или ID
    """
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'id']

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query.isdigit():
            return User.objects.filter(id=int(query))
        return User.objects.filter(username__icontains=query)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CharacterClassListUpdateAPIView(APIView):
    """
    GET  /api/users/character-classes/ — вернуть все классы + выбранные текущим пользователем
    PATCH /api/users/character-classes/ — обновить выбор классов
    """
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        classes = CharacterClass.objects.all()
        serializer = CharacterClassSerializer(classes, many=True, context={'request': request})

        selected_ids = []
        if request.user.is_authenticated:
            selected_ids = list(
                request.user.profile.character_classes.values_list('id', flat=True)
            )

        return Response({
            'classes': serializer.data,
            'selected_ids': selected_ids
        })

    def patch(self, request):
        ids = request.data.get('selected_ids')
        if not isinstance(ids, list):
            return Response(
                {'detail': 'Нужен список selected_ids'},
                status=status.HTTP_400_BAD_REQUEST
            )

        qs = CharacterClass.objects.filter(id__in=ids)
        if qs.count() != len(ids):
            return Response(
                {'detail': 'Один или несколько классов не найдены'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile = request.user.profile
        profile.character_classes.set(qs)
        profile.save()

        return Response({
            'selected_ids': list(profile.character_classes.values_list('id', flat=True))
        })