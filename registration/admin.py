from django.contrib import admin
from models import *

from views import count_payment
class UserPreferencesAdmin(admin.ModelAdmin):
    list_per_page = 200
    list_display = (
    'user',
    'total_cost',
    'ZOSIA_cost',
    'bus_cost',
    'days',
    'breakfasts',
    'dinners',
    'vegetarian',
    'shirt',
    'org',
    'minutes_early'
    )
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('bus_hour',)
    list_editable = ('minutes_early',)

    def anim_icon(self,id):
        return '<img src="/static_media/images/macthrob-small.png" alt="loading" id="anim%s" style="display:none"/>'%id
    yes_icon = '<img src="/static_media/images/icon-yes.gif" alt="Yes" />'
    no_icon  = '<img src="/static_media/images/icon-no.gif" alt="No" />'
    def onclick(self,id,obj):
        return u"""if(confirm('Do you want to register payment from %s?')) {
        document.getElementById('anim%s').style.display='inline';
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState  == 4) {
                document.getElementById('anim%s').style.display='none';
                if( xhr.status == 200) {
                    window.location.reload();
                }
            }
        };
        xhr.open('POST', '/admin/register_payment/', true);
        xhr.send('id=%s');
        }""" % (obj, id, id, id)
    def bus_onclick(self,obj):
        id = obj.id
        return u"""if(confirm('Do you want to register transport payment from %s?')) {
        //document.getElementById('anim%s').style.display='inline';
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState  == 4) {
                //document.getElementById('anim%s').style.display='none';
                if( xhr.status == 200) {
                    window.location.reload();
                }
            }
        };
        xhr.open('POST', '/admin/register_bus_payment/', true);
        xhr.send('id=%s');
        }""" % (obj, id, id, id)


    def total_cost(self, obj):
        r = self.no_icon
        if obj.paid and (obj.paid_for_bus or not obj.bus):
            r = self.yes_icon
        return u"%s %s&nbsp;z\u0142" % (r, (count_payment(obj)+40))
    total_cost.allow_tags = True

    def ZOSIA_cost(self, obj):
        if obj.paid:
            return u"%s %s&nbsp;z\u0142" % ( self.yes_icon, count_payment(obj) )
        else: 
            return u'<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a> %s' % (
                    self.onclick(obj.id,obj), self.no_icon, count_payment(obj), self.anim_icon(obj.id))
    ZOSIA_cost.allow_tags = True

    def bus_cost(self, obj):
        # if user doesn't wanna get but, so he shouldn't
        if not obj.bus:
            return "%s&nbsp;-" % self.no_icon
        elif obj.paid_for_bus:
            return u"%s %s&nbsp;z\u0142" % ( self.yes_icon, "40" )
        else: 
            return u'<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a>' % ( self.bus_onclick(obj), self.no_icon, "40" )
    bus_cost.allow_tags = True

    shirt_types = {}
    for i in 0,1:
        v = SHIRT_TYPES_CHOICES.__getitem__(i)
        shirt_types[v.__getitem__(0)] = v.__getitem__(1)
    def shirt(self, obj):
        return "%s (%s)" % (
                self.shirt_types[obj.shirt_type],
                obj.shirt_size)

    def f(self,o):
        def g(x):
            if o.__dict__[x]: return self.yes_icon
            else: return self.no_icon
        return g
    # note: these three methods should not be separated
    # but generated through lamba function
    # do it in spare time
    def breakfasts(self,obj):
        lst = ['breakfast_2', 'breakfast_3', 'breakfast_4']
        return "&nbsp;".join(map(self.f(obj),lst))
    breakfasts.allow_tags = True

    def dinners(self,obj):
        lst = ['dinner_1', 'dinner_2', 'dinner_3']
        return "&nbsp;".join(map(self.f(obj),lst))
    dinners.allow_tags = True

    def days(self,obj):
        lst = ['day_1', 'day_2', 'day_3']
        return "&nbsp;".join(map(self.f(obj),lst))
    days.allow_tags = True

admin.site.register(UserPreferences, UserPreferencesAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'name',
    'accepted'
    )
admin.site.register(Organization, OrganizationAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_per_page = 200
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
