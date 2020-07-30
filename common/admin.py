from django.contrib import admin
from common.models import User, Address, Comment, Comment_Files, Product
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Comment)
admin.site.register(Comment_Files)
admin.site.register(Product)
