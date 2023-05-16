"""API для работы с Алисой."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status

from services.assistant.alisa import Alisa, get_alisa

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Webhook для Алисы',
    description='Обработка запросов от Алисы',
)
async def alisa_handler(
        request: Request,
        assistant: Alisa = Depends(get_alisa),
):

    data = await request.json()

    return await assistant.handler(request=data)
