from django.db.models import F
from rest_framework.response import Response

from shortener.models import Users


def url_count_changer(request, is_crease: bool):
    count_number = 1 if is_crease else -1
    Users.objects.filter(user_id=request.user.id).update(
        url_count=F("url_count") + count_number
    )


def MsgOk(status: int = 200):
    return Response({"msg": "ok"}, status=status)
