from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse
from pages.models import GalleryImage, RSVP, Contact


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


def rsvp_view(request):
    if request.method == 'POST':
        rsvp = RSVP()
        rsvp.name = request.POST.get('rsvp_name')
        rsvp.email = request.POST.get('rsvp_email')
        rsvp.attendees = request.POST.get('rsvp_attendees')
        rsvp.pork = request.POST.get('rsvp_pork')
        rsvp.chicken = request.POST.get('rsvp_chicken')
        rsvp.vegetarian = request.POST.get('rsvp_vegetarian')
        rsvp.save()
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})


def contact_view(request):
    if request.method == 'POST':
        contact = Contact()
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.message = request.POST.get('message')
        contact.save()
    return HttpResponseRedirect(reverse('home'))
