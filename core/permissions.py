from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff
        
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("You don't have permission to view this page.")

def staff_required(view_func):
    def check_staff(user):
        if user.is_active and user.is_staff:
            return True
        if user.is_authenticated:
            raise PermissionDenied("You don't have permission to view this page.")
        return False
        
    return login_required(user_passes_test(check_staff)(view_func))
