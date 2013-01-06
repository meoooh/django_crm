# -*- coding: utf-8 -*-

from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class userRegistrationForm(forms.Form):
	userId = forms.CharField(label='아이디',
		max_length=30,
		)
	userName = forms.CharField(label='이름',
			max_length=70,
			)
	email = forms.EmailField(label='전자우편')
	mobile = forms.CharField(label='휴대전화번호',
			max_length=13
			)
	password1 = forms.CharField(label='비밀번호',
			widget=forms.PasswordInput(),
			)
	password2 = forms.CharField(label='비밀번호(확인)',
			widget=forms.PasswordInput(),
			)

	def clean_userId(self):
		if 'userId' in self.cleaned_data:
			if not re.search(r'^\w+$', self.cleaned_data['userId']):
				raise forms.ValidationError(
						'아이디는 알파벳, 숫자, 밑줄(_1)만 가능합니다.')
#			import pdb
#			pdb.set_trace()
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
			if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) == None: # re.search(a, b)는 b가 a와 일치 하지 않을때 None를 반환함.
				_mobile=''
				for i in mobile:
					if i.isdigit():
						_mobile+=i
				mobile=_mobile
				if re.search(r'^01(0|1|6|7|8|9)\d{7,8}$', mobile) == None:
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
