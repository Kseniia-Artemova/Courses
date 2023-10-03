from rest_framework import serializers

from courses.models import Course, Lesson, Payment
from courses.permissions import OnlyManagerOrOwner


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации об уроках"""

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(instance):
        if instance.user:
            return instance.user.email

    class Meta:
        model = Lesson
        # fields = '__all__'
        fields = ('name', 'description', 'user')
        permission_classes = [OnlyManagerOrOwner]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о курсах"""

    # Тут на всякий случай два варианта, чтобы оба в голове держать

    # lesson_count = serializers.IntegerField(source='lesson_set.all.count')
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    user = serializers.SerializerMethodField()

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    @staticmethod
    def get_user(instance):
        if instance.user:
            return instance.user.email

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lesson_count', 'lessons', 'user']
        permission_classes = [OnlyManagerOrOwner]


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о платежах"""

    class Meta:
        model = Payment
        fields = '__all__'
        permission_classes = [OnlyManagerOrOwner]