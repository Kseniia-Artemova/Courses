from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscription
from courses.permissions import OnlyManagerOrOwner
from courses.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации об уроках"""

    user = serializers.SerializerMethodField(read_only=True)
    video = serializers.URLField(validators=[LinkValidator()])

    @staticmethod
    def get_user(instance):
        if instance.user:
            return instance.user.email

    class Meta:
        model = Lesson
        # fields = '__all__'
        fields = ('name', 'description', 'video', 'user', 'course')
        # Не работает указание прав доступа в сериализаторе
        # permission_classes = [OnlyManagerOrOwner]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о курсах"""

    # Тут на всякий случай два варианта, чтобы оба в голове держать

    # lesson_count = serializers.IntegerField(source='lessons.all.count')
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    user = serializers.SerializerMethodField()
    is_updates_active = serializers.SerializerMethodField()

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    @staticmethod
    def get_user(instance):
        if instance.user:
            return instance.user.email

    def get_is_updates_active(self, instance):
        user = self.context['request'].user
        return instance.updates.filter(user=user).exists()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lesson_count', 'lessons', 'user', 'is_updates_active']
        # Не работает указание прав доступа в сериализаторе
        # permission_classes = [OnlyManagerOrOwner]


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о платежах"""

    class Meta:
        model = Payment
        exclude = ('id_stripe_session', )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о подписках на курс"""

    class Meta:
        model = Subscription
        fields = ('course', 'user')