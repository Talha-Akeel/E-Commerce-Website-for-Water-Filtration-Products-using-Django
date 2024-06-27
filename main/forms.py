from django import forms
from .models import UserAddressBook



# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','status')

