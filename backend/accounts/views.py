from django.http import JsonResponse

def your_view(request):
    data = {"message": "Your response data"}
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"  # Add the origin that needs access
    return response
