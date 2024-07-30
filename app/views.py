from django.shortcuts import render
import subprocess

from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('django')


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RCEView(View):
    @csrf_exempt
    def get(self, request):
        try:
            return JsonResponse({"message": f"env is {settings.SAMPLE_ENV.get()}"}, status=200)
        except Exception as e:
            logger.error("Error in RCEView: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        cmd = request.POST.get('cmd')
        try:
            output = subprocess.check_output(cmd.command, shell=True, text=True)
            print(cmd.command)
            return JsonResponse({"output": output}, status=200)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=418)
        except Exception as e:
            raise Exception(f"status_code=400, detail={str(e)}")


