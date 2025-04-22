from django.db import models
from config.settings import base


class TimeStampedModel(models.Model):
    """
    데이터 생성 및 수정 시각을 자동으로 관리하는 추상 모델 클래스
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SurveyQuestion(models.Model):
    """
    설문 문항을 저장하는 모델 (객관식/주관식, summary 포함)
    """
    QUESTION_TYPE_CHOICES = [
        ('single', '객관식 단일 선택'), # (DB 저장값, display 용 이름)
        ('multiple', '객관식 다중 선택'),
        ('text', '주관식'),
    ]

    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    summary = models.CharField(max_length=50, null=True, blank=True)  # LLM prompt에 보내기 위한 키
    required = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class SurveyOption(models.Model):
    """
    객관식 문항의 선택지를 저장하는 모델
    """
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100)

    def __str__(self):
        return self.option_text


class UserSurveyResponse(TimeStampedModel):
    """
    사용자가 설문을 제출한 기록을 저장하는 모델
    """
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} 응답"


class SurveyAnswer(models.Model):
    """
    설문 응답 중 각 문항에 대한 사용자의 개별 답변을 저장하는 모델
    """
    response = models.ForeignKey(UserSurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)

    # 모든 답변은 문자열로 저장
    # - 단일 선택: 문자열 1개
    # - 다중 선택: JSON 문자열로 저장 (ex. '["A", "B"]')
    # - 주관식: 자유 텍스트
    answer_text = models.TextField()

    def get_parsed_answer(self):
        try:
            return json.loads(self.answer_text)
        except:
            return self.answer_text


class ChatbotResponse(models.Model):
    """
    사용자가 여러 질문에 답변한 데이터를 저장하는 모델
    """
    custom_id = models.CharField(max_length=255, unique=True)  # 사용자 ID
    responses = models.JSONField()  # 질문과 답변을 JSON 형태로 저장
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시각

    def __str__(self):
        return f"Responses for {self.custom_id}"
