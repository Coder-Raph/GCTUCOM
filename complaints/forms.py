# complaints/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    # Replace the 'email' field with a 'student_id' field
    student_id = forms.CharField(label='Student ID', max_length=10)

    class Meta:
        model = Complaint
        fields = ['name', 'student_id', 'category', 'description', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Complaint'))

class CustomComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Include the 'email' field in the form
        self.fields['email'] = forms.EmailField()
        # Add crispy forms features if needed
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Complaint'))
