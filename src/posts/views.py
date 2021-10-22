from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.datastructures import MultiValueDictKeyError

from django.views.generic import ListView, CreateView
from posts.forms import BookArticle, ReviewForm
from posts.models import Ticket, Review, UserFollows
from itertools import chain

from utilisateurs.models import CustomUser


class CriticsHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/ticket_list.html'

    def get_queryset(self):
        follow = [self.request.user.id]
        users = CustomUser.objects.all()
        users_follow = UserFollows.objects.filter(user_id=self.request.user.id)
        for user in users_follow:
            for all_user in users:
                if all_user.id == user.followed_user_id:
                    follow.append(all_user.id)

        all_reviews = Review.objects.all()
        all_tickets = Ticket.objects.filter(user_id=self.request.user.id)
        review_id = []
        ticket_id = []
        for review in all_reviews:
            for ticket in all_tickets:
                if review.ticket_id == ticket.id:
                    review_id.append(review.id)
        for review in all_reviews:
            if review.user_id == self.request.user.id:
                ticket_id.append(review.ticket_id)

        tickets = Ticket.objects\
            .filter(Q(user_id__in=follow) | Q(id__in=ticket_id))
        reviews = Review.objects\
            .filter(Q(user_id__in=follow) | Q(id__in=review_id))
        for ticket in tickets:
            for user in users:
                if ticket.user_id == user.id:
                    ticket.username = user.username
        for review in reviews:
            for user in users:
                if review.user_id == user.id:
                    review.username = user.username
            for ticket in tickets:
                if review.ticket_id == ticket.id:
                    review.ticket = ticket
                    ticket.already = True

        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created, reverse=True)
        return result_list


class TicketCreate(CreateView):
    model = Ticket
    template_name = "posts/ticket_create.html"
    fields = ['title', 'description', 'image', ]

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        model_instance.save()
        model_instance.image = self.request.FILES['image']
        return HttpResponseRedirect('/home')


@login_required(login_url='/login')
def Review_form(request, ticket=None, review=None):
    reviews = None
    try:
        ticket = Ticket.objects.filter(id=ticket)[0]
    except IndexError:
        pass
    try:
        reviews = Review.objects.filter(id=review)[0]
    except IndexError:
        pass
    if request.method == 'POST':
        form = BookArticle(request.POST)
        formset = ReviewForm(request.POST)
        if form.is_valid() or formset.is_valid():
            if reviews is None:
                instance_review = formset.save(commit=False)
                try:
                    instance_ticket = form.save(commit=False)
                    instance_ticket.user_id = request.user.id
                    instance_ticket.image = request.POST['image']
                    instance_ticket.save()
                    instance_review.user_id = request.user.id
                    instance_review.ticket_id = instance_ticket.pk
                except ValueError:
                    instance_review.user_id = request.user.id
                    instance_review.ticket_id = ticket.id
                instance_review.save()
                return HttpResponseRedirect('/posts/')
            else:
                reviews.rating = request.POST.get('rating')
                reviews.headline = request.POST.get('headline')
                reviews.body = request.POST.get('body')
                reviews.save()
                return HttpResponseRedirect('/posts/')
    try:
        form_review = ReviewForm(
            initial={'headline': reviews.headline,
                     'rating': reviews.rating,
                     'body': reviews.body}
        )
    except AttributeError:
        form_review = ReviewForm()
    form_ticket = BookArticle()
    return render(request, "posts/review_create.html",
                  {"ticket_form": form_ticket,
                   "review_form": form_review,
                   "ticket": ticket})


class CriticsMyHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/mypost.html'

    def get_queryset(self):
        all_tickets = Ticket.objects.all()
        tickets = Ticket.objects.filter(user_id=self.request.user.id)
        reviews = Review.objects.filter(user_id=self.request.user.id)
        users = CustomUser.objects.all()
        for review in reviews:
            for ticket in all_tickets:
                if ticket.id == review.ticket_id:
                    review.ticket = ticket
        for review in reviews:
            review.username = self.request.user.username
        for ticket in tickets:
            ticket.username = self.request.user.username
        for user in users:
            for review in reviews:
                if review.ticket.user_id == user.id:
                    review.ticket.username = user.username
        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created, reverse=True)
        return result_list


@login_required(login_url='/login')
def delete(request, id):
    get_object_or_404(UserFollows, pk=id).delete()
    return HttpResponseRedirect('/followed')


@login_required(login_url='/login')
def delete_post(request, id):
    get_object_or_404(Ticket, pk=id).delete()
    return HttpResponseRedirect('/posts')


@login_required(login_url='/login')
def update_post(request, ticket):
    ticket_instance = Ticket.objects.filter(
        id=ticket)[0]
    form = BookArticle(initial={"title": ticket_instance.title,
                                "description": ticket_instance.description,
                                "image": ticket_instance.image})
    if request.method == 'POST':
        forms = BookArticle(request.POST)
        ticket0 = forms.save(commit=False)
        ticket_instance.title = ticket0.title
        ticket_instance.description = ticket0.description
        try:
            ticket_instance.image = request.FILES['image']
        except MultiValueDictKeyError:
            ticket_instance.image = ticket_instance.image
        ticket_instance.save()
        return HttpResponseRedirect('/posts')
    return render(request, "posts/ticket_create.html", {"form": form})


@login_required(login_url='/login')
def delete_review(request, id):
    get_object_or_404(Review, pk=id).delete()
    return HttpResponseRedirect('/posts')
