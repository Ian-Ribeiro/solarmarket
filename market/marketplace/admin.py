from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Produto)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "estoque")
    list_filter = ["categoria"]
    search_fields = ("nome",)
