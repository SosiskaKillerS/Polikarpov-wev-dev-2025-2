import re

phone_number1 = '7 910 458 09 12' # False
phone_number2 = '+7 (910) 458 09 12' # True
phone_number3 = '9 910 458 09 12' # False
phone_number4 = '9104580912' # True
phone_number5 = '9104580912@' # False
phone_number6 = '+7 910 458 09 12AB' # False

phone_numbers = [phone_number1,phone_number2,phone_number3,phone_number4,phone_number5, phone_number6]
for phone_number in phone_numbers:
    nums_from_phone_num = ''.join(re.findall(r'\d', phone_number))
    if re.search(r'[!~`@#$%^&*=_?/\\a-zA-Z]', phone_number):
        print(f"{phone_number}: {False} - спецсимволы или буквы в слове")
    elif (phone_number.startswith('+7') or phone_number.startswith('8')) and len(nums_from_phone_num)==11:
        print(f"{phone_number}: {True} - Корректный номер")
    elif len(nums_from_phone_num) == 10:
        print(f"{phone_number}: {True} - Все корректно")
    else:
        print(f"{phone_number}: {False} - что - то не так с кол-вом цифр")