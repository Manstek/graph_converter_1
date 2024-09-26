from django import forms

INPUT = ('Введите матрицу инцидентности, '
         'строки разделяйте новой строкой, элементы - пробелами.')


class IncidenceMatrixForm(forms.Form):
    matrix = forms.CharField(widget=forms.Textarea,
                             label='Введите матрицу инциденций',
                             help_text=INPUT)
