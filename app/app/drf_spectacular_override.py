excluded_paths = {
    "": "GET",
    "{id}/": ("GET", "PUT", "PATCH", "DELETE"),
    "activation/": "POST",
    "resend_activation/": "POST",
    "reset_email/": "POST",
    "reset_email_confirm/": "POST",
    "reset_password/": "POST",
    "reset_password_confirm/": "POST",
    "reset_username/": "POST",
    "reset_username_confirm/": "POST",
    "set_password/": "POST",
    "set_email/": "POST",
}

prefix = "/api/auth/users/"


def exclude_paths(endpoints):
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if not (
            path.removeprefix(prefix) in excluded_paths
            and method in excluded_paths.get(path.removeprefix(prefix))
        )
    ]
