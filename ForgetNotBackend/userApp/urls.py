from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('general/', include([
        path('contact/', views.get_contact_view),
    ])),
    path('user/', include([
        path("login/", views.authenticate),
        path('generate_verification_code/', views.generate_verification_code, name='generate_verification_code'),
        path("register/", views.register),
        path("get/", views.get_user_view),
        path("update/", views.update_user_view)
    ])),
    path("event/", include([
        path("create/", views.create_event_view),
        # for detail display
        # path("get/"),
        # for all display
        path("update/", views.update_event_view),
        path("get_list/", views.get_event_list),
        path("delete/", views.delete_event_view),
        path("invite/", views.invite_visitor),
        path("invite_list/", views.invite_list),
        path("get/", views.get_event_by_ref)
    ])),
    path('label/', include([
        path('get/', views.get_label_view),
        path('create/', views.create_label_view),
        path('delete/', views.delete_label_view),
        path('update/', views.update_label_view),
    ])),
    path('invite/', include([
        path('accept/', views.accept_invite),
        path('reject/', views.reject_invite)
    ]))
]
