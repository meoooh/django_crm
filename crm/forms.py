# -*- coding: utf-8 -*-

from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from crm.models import *
# from django.forms import ModelForm


class userRegistrationForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': '아이디'}),
    )

    name = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '이름'}),
    )

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '전자우편', 'type': 'email'}),
    )

    mobile = forms.CharField(
        label='',
        max_length=13,
        widget=forms.TextInput(attrs={'placeholder': '휴대전화번호'}),
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
    )

    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호(확인)'}),
    )

    def clean_userId(self):
        if 'userId' in self.cleaned_data:
            if not re.search(r'^\w+$', self.cleaned_data['userId']):
                raise forms.ValidationError(
                    '아이디는 알파벳, 숫자, 밑줄(_1)만 가능합니다.'
                )
#            import pdb
#            pdb.set_trace()
            try:
                User.objects.get(username=self.cleaned_data['userId'])
            except ObjectDoesNotExist:
                return self.cleaned_data['userId']
            raise forms.ValidationError('이미 등록된 아이디입니다.')
        else:
            raise forms.ValidationError('올바른 아이디가 아닙니다.')

    def clean_mobile(self):
        if 'mobile' in self.cleaned_data:
            mobile = self.cleaned_data['mobile']
            if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) is None:  # re.search(a, b)는 b가 a와 일치 하지 않을때 None를 반환함.
                _mobile = ''
                for i in mobile:
                    if i.isdigit():
                        _mobile += i
                mobile = _mobile
                if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) is None:
                    raise forms.ValidationError('올바른 휴대전화번호가 아닙니다.')
            return mobile
        else:
            raise forms.ValidationError('올바른 휴대전화번호가 아닙니다.')

    def clean_email(self):
        if 'email' in self.cleaned_data:
            try:
                User.objects.get(email=self.cleaned_data['email'])
            except ObjectDoesNotExist:
                return self.cleaned_data['email']
            raise forms.ValidationError('이미 등록된 전자우편입니다.')
        else:
            raise forms.ValidationError('올바른 전자우편이 아닙니다.')

    def clean_password2(self):
        if 'password1' and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] == self.cleaned_data['password2']:
                return self.cleaned_data['password1']
            else:
                raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        else:
            raise forms.ValidationError('올바른 비밀번호가 아닙니다.')


class WorkDailyRecordForm(forms.Form):
    ONGOING_OR_END = (
        ('ing', '진행중'),
        ('end', '완료'),
    )
    """
    ongoing_or_end = forms.ChoiceField(
            label='',
            choices=ONGOING_OR_END,
            initial ='ing',
            widget=forms.Select(attrs={'style': 'width:85px'}),
        )
    """
    contents = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': '내용', 'style': 'width:764px; height:35px;'}),
        required=False,
    )

    target_user = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '대상자', 'style': 'width:724px'}),
        required=False,
    )


class CustomerRegistrationForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '고객사 이름'}),
        required=False,
    )

    personInChargesName = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '담당자 이름'}),
        required=False,
    )

    personInChargesTel = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '담당자 전화번호'}),
        required=False,
    )

    personInChargesMobile = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '담당자 휴대전화'}),
        required=False,
    )

    personInChargesEmail = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '담당자 전자우편'}),
        required=False,
    )

    position = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '위치'}),
        required=False,
    )

    serviceName = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '서비스이름'}),
        required=False,
    )

    detailedServiceName = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '상세서비스이름'}),
        required=False,
    )

    serviceNumber = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '서비스번호'}),
        required=False,
    )

    dataFolder = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '폴더경로'}),
        required=False,
    )

    workers = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '작업자'}),
        required=False,
    )

    salespersons = forms.CharField(
        label='',
        min_length=1,
        widget=forms.TextInput(attrs={'placeholder': '담당영업'}),
        required=False,
    )

    notes = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': '비고', 'style': 'width:764px; height:35px;'}),
        required=False,
    )

    ipaddrs = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '호스트'}),
        required=False,
        min_length=1,
    )
    ipaddrsNote = forms.CharField(
        label='',
        min_length=1,
        widget=forms.TextInput(attrs={'placeholder': '호스트 비고'}),
        required=False,
    )

    domains = forms.URLField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '도메인'}),
        required=False,
    )

    domainsNote = forms.CharField(
        label='',
        min_length=1,
        widget=forms.TextInput(attrs={'placeholder': '도메인 비고'}),
        required=False,
    )

    types = (
        ('ids', 'IDS'),
        ('ips', 'IPS'),
        ('fw', '방화벽'),
        ('waf', '웹방화벽'),
        ('SW', '스위치'),
        ('ddos', 'Anti-DDos'),
        ('log', 'Log'),
        ('utm', 'UTM'),
        ('etc', '기타'),
    )

    equipmentsType = forms.ChoiceField(
        label='',
        choices=types,
        initial='ing',
        widget=forms.Select(),
        required=False,
    )

    equipmentsIpaddr = forms.GenericIPAddressField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '장비IP주소'}),
        required=False,
    )

    equipmentsNote = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder':  '장비정보', 'style': 'width:764px; height:35px;'}),
        required=False,
    )

    alertEmails = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '알람메일'}),
        required=False,
    )

    alertSMSs = forms.CharField(
        label='',
        max_length=70,
        widget=forms.TextInput(attrs={'placeholder': '알람문자'}),
        required=False,
    )

    def clean_name(self):
        if 'name' in self.cleaned_data:
            try:
                Customer.objects.get(name=self.cleaned_data['name'])
            except ObjectDoesNotExist:
                return self.cleaned_data['name']
            else:
                raise forms.ValidationError('고객사 이름이 존재합니다.')
            raise forms.ValidationError('비정상 동작')
        else:
            raise forms.ValidationError('올바른 고객사 이름이 아닙니다.')

    def clean_personInChargesMobile(self):
        if 'personInChargesMobile' in self.cleaned_data:
            mobile = self.cleaned_data['personInChargesMobile']
            if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) is None:  # re.search(a, b)는 b가 a와 일치 하지 않을때 None를 반환함.
                _mobile = ''
                for i in mobile:
                    if i.isdigit():
                        _mobile += i
                mobile = _mobile
                if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) is None:
                    raise forms.ValidationError('올바른 휴대전화번호가 아닙니다.')
            return mobile
        else:
            raise forms.ValidationError('올바른 휴대전화번호가 아닙니다.')

    def clean_workers(self):
        if 'workers' in self.cleaned_data:
            try:
                UserProfile.objects.get(name=self.cleaned_data['workers'])
            except ObjectDoesNotExist:
                raise forms.ValidationError('등록되지 않은 작업자 입니다.')
            else:
                return self.cleaned_data['workers']
                # return UserProfile.objects.get(name=self.cleaned_data['workers']).user
            raise forms.ValidationError('비정상 동작')
        else:
            raise forms.ValidationError('올바른 작업자가 아닙니다.')

    def clean_salespersons(self):
        if 'workers' in self.cleaned_data:
            try:
                UserProfile.objects.get(name=self.cleaned_data['salespersons'])
            except ObjectDoesNotExist:
                raise forms.ValidationError('등록되지 않은 담당영업 입니다.')
            else:
                return self.cleaned_data['salespersons']
                # return UserProfile.objects.get(name=self.cleaned_data['salespersons']).user
            raise forms.ValidationError('비정상 동작')
        else:
            raise forms.ValidationError('올바른 담당영업이 아닙니다.')


class ResponsingAttackDetectionForm(forms.Form):
    xss = "xs"
    sqlInjection = "sq"
    csrf = "cs"
    webshell = "we"
    defacement = "de"
    kinds = (
        (sqlInjection, 'sqlInjection'),
        (xss, 'XSS'),
        (csrf, 'CSRF'),
        (webshell, 'Webshell'),
        (defacement, 'Defacement'),
    )
    kind = forms.ChoiceField(
        label='',
        choices=kinds,
        initial=sqlInjection,
        widget=forms.Select(),
        required=False,
    )
    attackerIp = forms.GenericIPAddressField()
    victimIp = forms.GenericIPAddressField()
    customer = forms.CharField(max_length=255)
    emailRecipient = forms.CharField(
        max_length=255,
    )
    smsRecipient = forms.CharField(
        max_length=255,
    )
    note = forms.CharField(
        widget=forms.Textarea,
    )

    def clean_customer(self):
        if 'customer' in self.cleaned_data:
            try:
                Customer.objects.get(name=self.cleaned_data['customer'])
            except:
                print 'f'
                raise forms.ValidationError('등록되지 않은 고객사 입니다.')
            else:
                print 't'
                return self.cleaned_data['customer']
        else:
            raise form.ValidationError('오류')
