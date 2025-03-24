# core/pipeline.py
def save_profile_picture(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        picture_url = response.get('picture')
        if picture_url:
            user_social_auth = user.social_auth.get(provider='google-oauth2')
            extra_data = user_social_auth.extra_data
            extra_data['picture'] = picture_url
            user_social_auth.extra_data = extra_data
            user_social_auth.save()
