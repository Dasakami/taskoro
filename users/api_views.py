from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken

from .models import  CharacterClass
from .serializers import (
    CustomUserCreateSerializer,
    UserSearchSerializer,
    ProfileSerializer,
    CharacterClassSerializer,
)

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    """
    POST /api/auth/users/
    принимает: username, password, re_password, email, class_id
    """
    serializer_class = CustomUserCreateSerializer  
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user':     response.data,
            'access':   str(refresh.access_token),
            'refresh':  str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    POST /api/auth/jwt/create/
    принимает username + password, возвращает access/refresh
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
        })


class UserProfileAPIView(RetrieveAPIView):
    """
    GET /api/profile/  — данные профиля (включая character_classes)
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UpdateProfileAPIView(UpdateAPIView):
    """
    PATCH /api/profile/update/ — обновить остальные поля профиля
    (но не классы, они через /character-classes/)
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserSearchAPIView(ListAPIView):
    """
    GET /api/users/search/?q=… — поиск по username/id
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


class CharacterClassListUpdateAPIView(APIView):
    """
    GET  /api/character-classes/  — вернуть все классы + выбранные текущим пользователем
    PATCH /api/character-classes/ — обновить выбор классов у request.user.profile
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
