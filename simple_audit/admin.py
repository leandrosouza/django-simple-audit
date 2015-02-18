# -*- coding:utf-8 -*-
"""Admin related view."""

from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.utils.html import escape

from .models import Audit
from .signal import MODEL_LIST


class ContentTypeListFilter(SimpleListFilter):

    """Human-readable title.

    Which will be displayed in the
    right admin sidebar just above the filter options."""

    title = _('Object')
    parameter_name = 'content_type__id__exact'

    def lookups(self, request, model_admin):
        """Return a list of tuples.

        The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(ct.pk, ct.name) for ct in ContentType.objects.get_for_models(
            *MODEL_LIST).values()]

    def queryset(self, request, queryset):
        """Return a filtered queryset.

        Based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            qs = queryset.filter(content_type_id=self.value())
        else:
            qs = queryset
        return qs


class AuditAdmin(admin.ModelAdmin):

    """Audit Admin."""

    search_fields = ("description", "audit_request__request_id",
                     "obj_description", "object_id")
    list_display = ("format_date", "audit_content", "operation",
                    "audit_user", "audit_description", )
    list_filter = ("operation", ContentTypeListFilter,)

    def format_date(self, obj):
        """Return audit object date formated."""
        return obj.date.strftime('%d/%m/%Y %H:%M')

    format_date.short_description = _("Date")
    format_date.admin_order_field = 'date'

    def audit_description(self, audit):
        """Return audit object description."""
        desc = smart_text(
            "<br/>".join(escape(audit.description or "").split('\n')))
        return desc

    audit_description.allow_tags = True
    audit_description.short_description = smart_text(_("Description"))

    def audit_content(self, audit):
        """Return audit object content."""
        obj_string = (audit.obj_description or audit.content_object
                      or audit.content_object_save)

        return smart_text("<a title='{0}' href='{1}?content_type"
                          "__id__exact={2}&object_id__exact={4}'>"
                          "{3}: {4}</a>").format(
                _("Click to filter"),
                reverse('admin:simple_audit_audit_changelist'),
                audit.content_type.id,
                obj_string,
                audit.object_id
            )

    audit_content.short_description = _("Current Content")
    audit_content.allow_tags = True

    def audit_user(self, audit):
        """Return audit object user."""
        if audit.audit_request:
            user = "<a title='%s' href='%s?user=%d'>%s</a>" % (
                _("Click to filter"),
                reverse('admin:simple_audit_audit_changelist'),
                audit.audit_request.user.id, audit.audit_request.user
            )
        else:
            user = "%s" % _("Unknown")

        return smart_text(user)

    audit_user.admin_order_field = "audit_request__user"
    audit_user.short_description = _("User")
    audit_user.allow_tags = True

    def get_queryset(self, request):
        """QS."""
        request.GET = request.GET.copy()
        user_filter = request.GET.pop("user", None)
        qs = Audit.objects.prefetch_related(
            "audit_request", "audit_request__user")
        if user_filter:
            qs = qs.filter(audit_request__user__in=user_filter)
        return qs

    def has_add_permission(self, request):
        """Test permission."""
        return False

admin.site.register(Audit, AuditAdmin)
