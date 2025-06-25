from  django.shortcuts import redirect

def notLoggedUsers(view_fun):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fun(request, *args, **kwargs)
    return wrapper
    
def allowedUser(allowedGroup=[]):
    def decorator(view_fun):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.exists():
                userGroup = request.user.groups.all()[0].name
                if userGroup in allowedGroup:
                    return view_fun(request, *args, **kwargs)
                else:
                    return redirect('login')
        return wrapper
    return decorator


def forAdmins(view_fun):
    def wrapper(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            
            group = request.user.groups.all()[0].name
        if  group =='admin':
            return view_fun(request, *args, **kwargs)
        if  group == 'customer':
            return redirect('no_permission')
        
    return wrapper
    
