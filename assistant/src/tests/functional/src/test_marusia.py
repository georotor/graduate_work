import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio

url = "/api/v1/marusia/"
base_request = {
  "session": {
    "session_id": "29bdbd6f-b8da-4c74-b1ac-76f11b370b88",
    "user_id": "286c50ea2b4e7d64e62d759908e46dde67c67c56b7c2456a3501ea06c5002251",
    "skill_id": "52401ef1-935a-49ef-bd57-1f3f83ac3447",
    "new": True,
    "message_id": 0,
    "application": {
      "application_id": "286c50ea2b4e7d64e62d759908e46dde67c67c56b7c2456a3501ea06c5002251",
      "application_type":"web",
    },
    "auth_token": "636d5f7d6fb18e1aff48bb161ab82de12012fec213a0bf2e9a9efd8b7825c69c",
    "user": {
      "user_id": "d36d8a3e-3431-4b5d-89d1-d9eac162ebdd"
    }
  },
  "request": {
    "command": "",
    "original_utterance": "",
    "nlu": {
      "tokens": [],
      "entities": []
    }
  },
  "state": {
    "session": {},
    "user": {}
  },
  "version": "1.0"
}


async def test_welcome(make_json_request):
    response = await make_json_request(url=url, json=base_request, method='post')

    assert response.status == HTTPStatus.OK
    assert response.body["session_state"]["dialog"] == "Welcome"
    assert "Справка по фильмам кинотеатра" in response.body["response"]["text"]
    assert response.body["response"]["end_session"] is False


async def tests_film_length(make_json_request):
    request = dict(base_request)
    request["session"]["new"] = False
    request["request"] = {
      "command": "сколько длится фильм матрица",
      "original_utterance": "сколько длится фильм матрица",
      "nlu": {
        "tokens": [],
        "entities": []
      }
    }

    response = await make_json_request(url=url, json=request, method='post')

    assert response.status == HTTPStatus.OK
    assert response.body["session_state"]["dialog"] == "Welcome"
    assert response.body["session_state"]["film"].lower() == "матрица"
    assert "длится" in response.body["response"]["text"]


async def tests_film_director(make_json_request):
  request = dict(base_request)
  request["session"]["new"] = False
  request["request"] = {
    "command": "кто режессировал фильм матрица",
    "original_utterance": "кто режессировал фильм матрица",
    "nlu": {
      "tokens": [],
      "entities": []
    }
  }

  response = await make_json_request(url=url, json=request, method='post')

  assert response.status == HTTPStatus.OK
  assert response.body["session_state"]["dialog"] == "Welcome"
  assert response.body["session_state"]["film"].lower() == "матрица"
  assert "режиссировал" in response.body["response"]["text"]
