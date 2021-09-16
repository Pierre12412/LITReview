from django.contrib import admin


from posts.models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','description','image','time_created','user_id',)

admin.site.register(Ticket,TicketAdmin)