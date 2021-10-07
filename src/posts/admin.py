from django.contrib import admin


from posts.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',
                    'image', 'time_created', 'user_id',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'user',
                    'headline', 'body', 'time_created')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)
