"""API для работы с Алисой."""

import logging

from fastapi import APIRouter, Depends

from models.assist import AssistRequest, AssistResponse
from services.assist import Assist, get_assist

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Webhook для Алисы',
    description='Обработка запросов от Алисы',
    response_model=AssistResponse
)
async def alisa_handler(
        request: AssistRequest,
        assist: Assist = Depends(get_assist),
):
    return await assist.handler(request=request)
