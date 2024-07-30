from django.shortcuts import render
import subprocess

from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from app.utils import SecurityLogger, LogHandler

logger = logging.getLogger('django')


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RCEView(View):
    backup_logger: SecurityLogger = SecurityLogger.get_instance("RCEView")
    log_handler: LogHandler = LogHandler.get_instance()

    @csrf_exempt
    def get(self, request):
        try:
            self.log_handler.info({
                "message": "something",
                "ip_addr": "192.156.1.23",
                "status": 200
            }, self.backup_logger)
            return JsonResponse({"message": f"env is {settings.SAMPLE_ENV.get()}"}, status=200)
        except Exception as e:
            logger.error("Error in RCEView: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.log_handler.info({
            "message": "something",
            "ip_addr": "192.156.1.23",
            "status": 500
        }, self.backup_logger)
        data = json.loads(request.body.decode('utf-8'))
        cmd = data.get('cmd')
        print(cmd)
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            print(cmd)
            return JsonResponse({"output": output}, status=200)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=418)
        except Exception as e:
            raise Exception(f"status_code=400, detail={str(e)}")


