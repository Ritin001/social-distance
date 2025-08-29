from django.shortcuts import render
from django.http import StreamingHttpResponse
from .detector import detect_social_distancing, load_model_once

def index(request):
    """
    Renders the main webpage with the video stream.
    """
    return render(request, 'detector_app/index.html')

def video_feed(request):
    """
    This function streams the video frames from the detector script.
    """
    model = load_model_once()
    if model is None:
        return StreamingHttpResponse(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n\r\n',
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    
    return StreamingHttpResponse(
        detect_social_distancing(model), # <-- This is the corrected line
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
