# Filepath: demo_Xinyang_Li_Week2/django-demo-project/my_demo_app/pipeline.py
from social_core.exceptions import AuthAlreadyAssociated
from django.contrib.auth import logout
from .models import LoggedInUser


def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)

    if social:
        if user and social.user != user:
            msg = "This account is already in use."
            raise AuthAlreadyAssociated(backend, msg)

        if not user:
            user = social.user

        # Log out the currently logged-in user if there is one
        try:
            current_logged_in_user = LoggedInUser.objects.get()
            logout(backend.strategy.request)
            current_logged_in_user.delete()
        except LoggedInUser.DoesNotExist:
            pass

        # Manually set the backend attribute on the user object
        user.backend = f"social_core.backends.{provider}.{provider.capitalize()}OAuth2"

        # Log in the new user and update the LoggedInUser model
        backend.strategy.session["_auth_user_id"] = user.pk
        backend.strategy.session["_auth_user_backend"] = user.backend
        LoggedInUser.objects.create(user=user)

    return {"social": social, "user": user}
