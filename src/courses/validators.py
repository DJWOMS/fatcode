from rest_framework import serializers


class StudentWorkValidator:

    def __call__(self, data):
        lesson_type = data['lesson'].lesson_type
        if 'quiz_answer' in data and not 'quiz' in lesson_type :
            raise serializers.ValidationError({'error': 'Урок не содержит quiz'})
        elif not data.keys() & {'code_answer', 'quiz_answer'}:
            raise serializers.ValidationError({'error': f'Ответ должен содержать {lesson_type}'})
        elif 'quiz' in lesson_type and 'code_answer' in data:
            raise serializers.ValidationError({'error': 'Нужен квиз'})
        if 'quiz' in data:
            if data['quiz_answer'].lesson != data['lesson']:
                raise serializers.ValidationError({'error': 'Квиз не из этого урока'})

