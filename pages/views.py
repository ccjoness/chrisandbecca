from django.shortcuts import render, HttpResponseRedirect, reverse
from pages.models import GalleryImage


def home(request):
    images = GalleryImage.objects.all()
    print(images)
    return render(request, 'pages/index.html', {'images': images})


def upload_photos(request):
    if request.method == 'POST':
        for f in request.FILES.getlist('images'):
            new_photo = GalleryImage()
            new_photo.image = f
            new_photo.save()
    return HttpResponseRedirect(reverse('home'))
