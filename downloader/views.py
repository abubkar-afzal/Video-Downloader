from django.shortcuts import render
from django.http import JsonResponse
from .forms import YouTubeForm, InstagramForm
import yt_dlp as youtube_dl
import instaloader
import os
import re
import platform

# Global variable to store progress
progress = 0

def get_downloads_folder():
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif platform.system() == "Darwin":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")

def home(request):
    return render(request, 'downloader/home.html')

def download_youtube(request):
    global progress
    progress = 0
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            location = form.cleaned_data['location']
            if not location:
                location = get_downloads_folder()
            else:
                os.makedirs(location, exist_ok=True)
            try:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': os.path.join(location, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                progress = 100
                return render(request, 'downloader/success.html', {'title': 'YouTube Video', 'location': location})
            except Exception as e:
                return render(request, 'downloader/error.html', {'error': str(e)})
        else:
            return render(request, 'downloader/youtube.html', {'form': form})
    else:
        form = YouTubeForm()
        return render(request, 'downloader/youtube.html', {'form': form})

def download_instagram(request):
    global progress
    progress = 0
    if request.method == 'POST':
        form = InstagramForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            location = form.cleaned_data['location']
            if not location:
                location = get_downloads_folder()
            else:
                os.makedirs(location, exist_ok=True)
            try:
                L = instaloader.Instaloader()
                L.dirname_pattern = location
                post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])

                # Progress simulation (instaloader doesn't provide progress callback)
                progress = 50  # Just an example, this should be updated accordingly
                L.download_post(post, target=location)
                progress = 100
                return render(request, 'downloader/success.html', {'title': post.title, 'location': location})
            except Exception as e:
                return render(request, 'downloader/error.html', {'error': str(e)})
        else:
            return render(request, 'downloader/instagram.html', {'form': form})
    else:
        form = InstagramForm()
        return render(request, 'downloader/instagram.html', {'form': form})

def get_progress(request):
    global progress
    return JsonResponse({'progress': progress})

def progress_hook(d):
    global progress
    if d['status'] == 'downloading':
        percent_str = d['_percent_str']
        # Remove ANSI color codes
        percent_str = re.sub(r'\x1b\[.*?m', '', percent_str)
        progress = int(float(percent_str.strip().strip('%')))
 