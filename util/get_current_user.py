def current_user(context):
    requestObj = context.get("request", None)
    if requestObj.user.is_anonymous:
        return ""
    else:
        return requestObj.user
