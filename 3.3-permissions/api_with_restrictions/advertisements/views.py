from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .permissions import IsOwnerOrReadOnly
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    throttle_classes = [UserRateThrottle]
    filterset_fields = ["creator"]


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
