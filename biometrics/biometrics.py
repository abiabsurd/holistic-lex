SEX_CHOICES = {
    'F': 'Female',
    'M': 'Male',
}

BODY_FRAME_TYPE_CHOICES = {
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large'
}

ACTIVITY_RATINGS = [
    'Sedentary (Little or no exercise)',
    'Lightly Active (Light exercise or sports 1 to 3 days per week)',
    'Moderately Active (Moderate exercise or sports 3 to 5 days per week)',
    'Very Active (Hard exercise or sports 6 to 7 days per week)',
    'Extra Active (Very hard exercise or sports 6 to 7 days per week + Physical job)'
]


def get_bmr_multiple(activity_rating):
    if activity_rating not in range(5):
        raise ValueError('Must pass value between 0 (Sedentary) and 4 (Extra Active)')

    return 1.2 + activity_rating * 0.175


def to_kg(pounds):
    return pounds * 0.453592


def to_cm(inches):
    return inches * 2.54


def ideal_protein(weight_in_kg):
    """in grams"""
    return 0.8 * weight_in_kg


def basal_metabolic_rate(weight_in_kg, height_in_cm, age):
    """in kcal"""
    return 10 * weight_in_kg + 6.25 * height_in_cm - 5 * age - 161


def hamwi_ideal_weight(sex, height, body_frame_type):
    for v, choices in ((sex, SEX_CHOICES), (body_frame_type, BODY_FRAME_TYPE_CHOICES)):
        if v not in choices:
            raise ValueError('"{}" is not a valid choice from: {}'.format(v, choices))

    base_height = 60  # 5 ft
    if height < base_height:
        raise ValueError('Unable to calculate for heights < 5 ft')

    sign_of_body_frame_type_multiplier = {
        'S': -1,
        'M': 0,
        'L': 1
    }
    body_frame_type_multiplier = 1 + 0.1 * sign_of_body_frame_type_multiplier[body_frame_type]

    sex_base_and_multiplier = {
        'M': (106, 6),
        'F': (100, 5)
    }
    sex_base, sex_mult = sex_base_and_multiplier[sex]

    return (sex_base + sex_mult * (height - base_height)) * body_frame_type_multiplier


def comparison_percentage(actual, ideal):
    return round(100 * actual / ideal, 2)


def proportion(value, percentage):
    return round(value * (percentage / 100), 2)


def thermic_effect_of_activity(bmr, bmr_multiple):
    return bmr * (bmr_multiple - 1)


def thermic_effect_of_food(bmr):
    return 0.1 * bmr


def total_energy_expenditure(bmr, tea, tef):
    return sum((bmr, tea, tef))
