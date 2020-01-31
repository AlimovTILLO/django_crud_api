from django.contrib import admin
from django.urls import path, reverse
from .models import Product, User
from .forms import ProductForm, UserChangeForm, UserCreationForm
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.utils import unquote


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'avatar',
            )
        }),
        ('Permissions', {
            'fields': ('is_admin', )
        }),
    )

    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'first_name', 'last_name', 'avatar', 'password1',
                   'password2')
    }), )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'color', 'pantone_value']
    list_filter = ['name', 'year', 'color']

    search_fields = ['name', 'year']
    form = ProductForm

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Product, ProductAdmin)