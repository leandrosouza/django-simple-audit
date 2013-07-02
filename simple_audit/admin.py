# -*- coding:utf-8 -*_
from django.contrib import admin
from django.utils.html import escape
from django.core.urlresolvers import reverse
from .models import Audit


class AuditAdmin(admin.ModelAdmin):
    search_fields = ("audit_request__user__username", "description", "audit_request__request_id", )
    list_display = ("audit_date", "audit_content", "operation", "audit_user", "audit_description", )
    list_filter = ("operation", "content_type",)

    def audit_description(self, audit):
        desc = "<br/>".join(escape(audit.description or "").split('\n'))
        return desc
    audit_description.allow_tags = True
    audit_description.short_description = "Description"

    def audit_content(self, audit):
        if audit.content_object:
            obj_string = audit.content_object
        else:
            obj_string = u""

        return "<a title='Click to filter' href='%(base)s?content_type__id__exact=%(type_id)s&object_id__exact=%(id)s'>%(type)s: %(obj)s</a>" % {
            'base': reverse('admin:simple_audit_audit_changelist'),
            'type': audit.content_type,
            'type_id': audit.content_type.id,
            'obj': obj_string,
            'id': audit.object_id}
    audit_content.short_description = "Current Content"
    audit_content.allow_tags = True

    def audit_date(self, audit):
        return audit.audit_request.date
    audit_date.admin_order_field = "audit_request__date"
    audit_date.short_description = u"Date"

    def audit_user(self, audit):
        return u"<a title='Click to filter' href='%s?user=%d'>%s</a>" \
            % (reverse('admin:simple_audit_audit_changelist'), audit.audit_request.user.id, audit.audit_request.user)
    audit_user.admin_order_field = "audit_request__user"
    audit_user.short_description = u"User"
    audit_user.allow_tags = True

    def queryset(self, request):
        request.GET = request.GET.copy()
        user_filter = request.GET.pop("user", None)
        qs = Audit.objects.prefetch_related("audit_request", "audit_request__user")
        if user_filter:
            qs = qs.filter(audit_request__user__in=user_filter)
        return qs

admin.site.register(Audit, AuditAdmin)
