from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.template.loader import render_to_string

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

        email_html = render_to_string('mailer.html', {'username': rsvp.name})
        email = EmailMessage(
            subject='Thank you for your RSVP',
            body=email_html,
            from_email='mail@chrisandbecca.com',
            to=[rsvp.email],
            reply_to=['mail@chrisandbecca.com'],
            headers={'Content-Type': 'text/html'},
        )
        email.content_subtype = "html"
        email.send()
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})


def contact_view(request):
    if request.method == 'POST':
        contact = Contact()
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.message = request.POST.get('message')
        contact.save()

        email = EmailMessage(
            subject='New Message from ChrisAndBecca.com',
            body=contact.message,
            from_email='mail@chrisandbecca.com',
            to=['chris.charles.jones@gmail.com', 'beccabeddingfield@gmail.com'],
            reply_to=[contact.email],
            headers={'Content-Type': 'text/plain'},
        )
        email.send()

    return HttpResponseRedirect(reverse('home'))


@login_required
def dashboard_view(request):
    all_rsvp = RSVP.objects.all()
    sum_attendees = RSVP.objects.aggregate(Sum('attendees'))
    sum_pork = RSVP.objects.aggregate(Sum('pork'))
    sum_chicken = RSVP.objects.aggregate(Sum('chicken'))
    sum_vegetarian = RSVP.objects.aggregate(Sum('vegetarian'))
    contacts = Contact.objects.all()
    return render(request, 'pages/dashboard.html', {
        'rspvs': all_rsvp,
        'sum_attendees': sum_attendees.get('attendees__sum'),
        'sum_pork': sum_pork.get('pork__sum'),
        'sum_chicken': sum_chicken.get('chicken__sum'),
        'sum_vegetarian': sum_vegetarian.get('vegetarian__sum'),
        'contacts': contacts
    })
