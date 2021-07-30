from app_users.forms import LoginForm


def log_form(request):
    login_form = LoginForm()
    return {'login_form': login_form}
