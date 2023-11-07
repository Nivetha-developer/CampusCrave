from rest_framework_simplejwt.tokens import RefreshToken, Token,AccessToken
from django.shortcuts import HttpResponse
import json
def auth_token(user,request):
    
   access = AccessToken.for_user(user)
   refresh=RefreshToken.for_user(user)
   return {"access_token": str(access),
   "refresh_token":str(refresh)}



def APIResponse(data,http_code, error=True, json_format=True):
    if error:
        status = 'OK'
        response = {
            "data": data,
            "status": status,
            "http_code": http_code
        }
        # http_code=200
    else:
        status = 'ERROR'
        # http_code=404
        response = {
            "data": data,
            "status": status,
            "http_code":http_code
        }
    if json_format:
        response = json.dumps(response)

    return HttpResponse(response, content_type='Application/json', status=int(http_code))
