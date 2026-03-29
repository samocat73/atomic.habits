
from rest_framework import serializers

from habit_tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        related_habit = data.get("related_habit")
        award = data.get("award")
        if related_habit and award:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Нельзя одновременно указывать поле related_habit и поле award."
                }
            )
        if related_habit:
            if not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    {
                        "related_habit": "Связанная привычка должна иметь признак приятной привычки (is_pleasant=True)."
                    }
                )
            if related_habit.award or related_habit.related_habit:
                raise serializers.ValidationError(
                    {
                        "related_habit": "У приятной привычки не может быть вознаграждения или связанной привычки."
                    }
                )
        return data
