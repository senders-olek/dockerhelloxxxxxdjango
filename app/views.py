from django.shortcuts import render
import subprocess
from django.views import View
from django.http import JsonResponse
from django.conf import settings

# Create your views here.

class RCEView(View):
    def get(self, request):
        try:
            return {"message": f"env is {settings.SAMPLE_ENV.get()}"}
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def post(self, request, *args, **kwargs):
        cmd = request.data.GET('cmd')
        try:
            output = subprocess.check_output(cmd.command, shell=True, text=True)
            print(cmd.command)
            return JsonResponse({"output": output})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)})
        except Exception as e:
            raise Exception(f"status_code=400, detail={str(e)}")


