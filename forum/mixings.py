from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect



# міксина для перевірки чи користувач має роль адміна
class WorkerOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'
    

class Login(LoginRequiredMixin):
    login_url = settings.LOGIN_URL




    def logint(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
