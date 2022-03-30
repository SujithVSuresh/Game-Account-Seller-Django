from django.contrib import admin
from .models import ListedGames, GameAccounts, CartOrder, CartItem, PostImage
# Register your models here.
admin.site.register(ListedGames)
admin.site.register(CartOrder)
admin.site.register(CartItem)

class PostImageAdmin(admin.StackedInline):
    model = PostImage
 
@admin.register(GameAccounts)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]
 
    class Meta:
       model = GameAccounts

admin.site.register(PostImage)       
