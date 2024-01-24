from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import re

@api_view(['GET'])
def generated_cpf(request):

    random_digits = ''
    for i in range(9):
        random_digits += str(random.randint(0, 9))

    weight_1 = 10
    checksum_1 = 0

    for digit in random_digits:
        checksum_1 += int(digit) * weight_1
        weight_1 -= 1

    digit_1 = (checksum_1 * 10) % 11
    digit_1 = digit_1 if digit_1 <= 9 else 0

    digits_with_1 = random_digits + str(digit_1)

    weight_2 = 11
    checksum_2 = 0

    for digit in digits_with_1:
        checksum_2 += int(digit) * weight_2
        weight_2 -= 1

    digit_2 = (checksum_2 * 10) % 11
    digit_2 = digit_2 if digit_2 <= 9 else 0

    cpf_generated = f'{random_digits}{digit_1}{digit_2}'
    return Response({"cpf": cpf_generated})

@api_view(['POST'])
def validate_cpf(request):
    input_cpf = request.data.get('cpf')

    sanitized_cpf = re.sub(r'[^0-9]', '', input_cpf)
    first_nine_digits = sanitized_cpf[:9]
    multiplier = 10
    result_first_digit = 0

    for digit in first_nine_digits:
        result_first_digit += int(digit) * multiplier
        multiplier -= 1
    calculated_first_digit = (result_first_digit * 10) % 11
    calculated_first_digit = calculated_first_digit if calculated_first_digit <= 9 else 0

    cpf_with_first_digit = first_nine_digits + str(calculated_first_digit)
    multiplier_second = 11
    result_second_digit = 0

    for digit_second in cpf_with_first_digit:
        result_second_digit += int(digit_second) * multiplier_second
        multiplier_second -= 1
    calculated_second_digit = (result_second_digit * 10) % 11
    calculated_second_digit = calculated_second_digit if calculated_second_digit <= 9 else 0

    generated_cpf = f'{first_nine_digits}{calculated_first_digit}{calculated_second_digit}'

    if input_cpf == generated_cpf:
        return Response({'CPF': 'valido'})
    else:
        return Response({'CPF': 'invalido'})
