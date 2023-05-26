import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio

url = "/api/v1/alisa/"
base_request = {
  "session": {
    "message_id": 0,
    "session_id": "559ebd2d-ddfd-469d-9848-112ec161072b",
    "skill_id": "3d6630a9-d3c0-416c-a9b5-dd856d5eeb76",
    "user": {
      "user_id": "A9082D2D8EC3A6435EEB61A4668C517CDF3ADE9CB09CEF6B8D38F224917C9888"
    },
    "application": {
      "application_id": "B7C1718C384C306728365ACCF8D59925EE095031631762584F922CDD540BE6D1"
    },
    "user_id": "B7C1718C384C306728365ACCF8D59925EE095031631762584F922CDD540BE6D1",
    "new": True
  },
  "request": {
    "command": "",
    "original_utterance": "",
    "nlu": {
      "tokens": [],
      "entities": [],
      "intents": {}
    }
  },
  "state": {
    "session": {},
    "user": {},
    "application": {}
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
        "entities": [],
        "intents": {
          "film_length": {
            "slots": {
              "film": {"value": "матрица"}
            }
          }
        }
      }
    }

    response = await make_json_request(url=url, json=request, method='post')

    assert response.status == HTTPStatus.OK
    assert response.body["session_state"]["dialog"] == "Welcome"
    assert response.body["session_state"]["film"] == "матрица"
    assert "длится" in response.body["response"]["text"]


async def tests_film_director(make_json_request):
  request = dict(base_request)
  request["session"]["new"] = False
  request["request"] = {
    "command": "кто режиссер фильма матрица",
    "original_utterance": "кто режиссер фильма матрица",
    "nlu": {
      "tokens": [],
      "entities": [],
      "intents": {
        "film_director": {
          "slots": {
            "film": {"value": "матрица"}
          }
        }
      }
    }
  }

  response = await make_json_request(url=url, json=request, method='post')

  assert response.status == HTTPStatus.OK
  assert response.body["session_state"]["dialog"] == "Welcome"
  assert response.body["session_state"]["film"] == "матрица"
  assert "режиссировал" in response.body["response"]["text"]
