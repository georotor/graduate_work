"""API для работы с Марусей."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.assist import AssistRequest, AssistResponse
from services.assist import Assist, get_assist

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Webhook для Маруси',
    description='Обработка запросов от Маруси',
)
async def alisa_handler(
        request: AssistRequest,
        assist: Assist = Depends(get_assist)
):

    # data = await request.json()
    print(request)

    return await assist.handler(request=request)

    # response = AssistResponse(
    #     **request.dict(),
    #     response={'text': 'Ку-ку'}
    # )
    #
    # return response

