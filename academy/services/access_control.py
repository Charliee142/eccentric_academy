# academy/services/access_control.py
def user_has_course_access(user, course):
    if not hasattr(user, 'planenrollment'):
        return False

    return user.planenrollment.plan == course.plan
