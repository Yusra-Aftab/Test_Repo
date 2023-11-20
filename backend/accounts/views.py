from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.settings import MEDIA_ROOT
from accounts.transcription import process
from accounts.summarization import summarize
from accounts.models import Video
from accounts.models import Summary
import os

@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        name = request.POST.get('name')  # Get the name from the request

        print(name)


        # Make sure the name is not empty
        if not name:
            return JsonResponse({'message': 'Name is required.'}, status=400)

        video_path = os.path.join(MEDIA_ROOT, video_file.name)
        with open(video_path, 'wb') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        # Now, you have the video file saved in the "media" folder
        # Pass the video_path and name to the process function in transcription.py
        transcript = process(video_path)
        print("Complete_Text")
        print(transcript)


        # Create and save an instance of the Video model
        video_instance = Video(name=name, transcript=transcript)
        video_instance.save()

        
        summary = summarize(transcript)
        print(summary)


        summary_instance = Summary(name=name, summary=summary)
        summary_instance.save()

        # Return a response, for example:
        return JsonResponse({'message': 'Video uploaded and transcription started.'})
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)



def get_video_names(request):
    # Retrieve a list of video names from the database
    video_names = Video.objects.values('id', 'name')
    return JsonResponse({'videos': list(video_names)})

def get_transcript(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
        return JsonResponse({'name': video.name, 'transcript': video.transcript})
    except Video.DoesNotExist:
        return JsonResponse({'message': 'Video not found'}, status=404)
    


def get_summary_names(request):
    # Retrieve a list of Summary names from the database
    summary_names = Summary.objects.values('id', 'name')
    return JsonResponse({'summaries': list(summary_names)})



def get_summary(request, summary_id):
    try:
        summary = Summary.objects.get(id=summary_id)
        return JsonResponse({'name': summary.name, 'summary': summary.summary})
    except Summary.DoesNotExist:
        return JsonResponse({'message': 'Summary not found'}, status=404)
