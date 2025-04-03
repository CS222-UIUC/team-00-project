# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_name = default_storage.save(f"uploads/{file.name}", file)
        file_url = default_storage.url(file_name)
        return JsonResponse(
            {"message": "File uploaded successfully", "file_url": file_url}
        )
    return JsonResponse({"error": "No file uploaded"}, status=400)
