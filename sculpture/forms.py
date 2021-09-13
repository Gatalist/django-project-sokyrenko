from django import forms

from .models import Reviews, PlaceOder


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class NewOrderForm(forms.ModelForm):
    """Форма заказа"""
    class Meta:
        model = PlaceOder
        fields = ('first_name', 'last_name', 'phone', 'email', 'text')
