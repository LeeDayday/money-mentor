from django.db import models


class TimeStampedModel(models.Model):
    """
    데이터 생성 및 수정 시각을 자동으로 관리하는 추상 모델 클래스
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
