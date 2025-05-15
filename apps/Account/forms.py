from django import forms


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(label="ایمیل شرکت", max_length=254, error_messages={
            'required': 'لطفاً ایمیل را وارد کنید.',
            'invalid': 'فرمت ایمیل وارد شده معتبر نیست.'
    })
