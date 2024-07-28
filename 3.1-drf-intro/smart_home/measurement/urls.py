from django.urls import path

from measurement.views import SensorListAPIView, SensorRetrieveUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    path('sensors/', SensorListAPIView.as_view(), name='sensor-list'),
    path('sensors/<int:pk>/', SensorRetrieveUpdateAPIView.as_view(), name='sensor-detail'),
    path('measurements/', MeasurementCreateAPIView.as_view(), name='measurement-create'),
]
