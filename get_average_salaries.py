def get_average_salaries(payment_form, payment_to):

    if payment_form and payment_to:
        return (payment_form + payment_to)/2
    elif payment_form:
        return payment_form*1.2
    else:
        return payment_to*0.8
