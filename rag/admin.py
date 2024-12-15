from django.contrib import admin
from .models import ChatbotResponse


@admin.register(ChatbotResponse)
class ChatbotResponseAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'created_at', 'updated_at')  # Admin 패널에서 표시할 필드
    search_fields = ('custom_id',)  # 검색 가능 필드
    list_filter = ('created_at',)  # 필터링 가능한 필드
