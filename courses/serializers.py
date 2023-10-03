from rest_framework import serializers

from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации об уроках"""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о курсах"""

    # Тут на всякий случай два варианта, чтобы оба в голове держать

    lesson_count = serializers.IntegerField(source='lesson_set.all.count')
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lesson_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки информации о платежах"""

    class Meta:
        model = Payment
        fields = '__all__'