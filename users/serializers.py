from rest_framework import serializers

from courses.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о пользователе"""

    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'payments']