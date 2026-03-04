from django.shortcuts import render
from django.http import JsonResponse
import io
import contextlib
import json

def editor_home(request):
    return render(request, 'editor/editor_home.html')


def run_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get('code', '')

        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code)
            result = output.getvalue()
        except Exception as e:
            result = str(e)

        return JsonResponse({"result": result})