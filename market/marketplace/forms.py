from django import forms
from .models import Categoria, Produto

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome", "descricao"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "categoria", "preco", "descricao", "estoque", "imagem"]
