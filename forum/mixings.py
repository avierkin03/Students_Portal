from django.contrib.auth.mixins import UserPassesTestMixin



# міксина для перевірки чи користувач має роль адміна
class WorkerOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'