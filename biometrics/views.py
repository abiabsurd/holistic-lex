from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render


from biometrics.biometrics import (
    get_bmr_multiple, ideal_protein, to_kg, to_cm, basal_metabolic_rate,
    comparison_percentage, thermic_effect_of_activity, thermic_effect_of_food,
    total_energy_expenditure, proportion
)
from biometrics.models import Client, Entry

json_encoder = DjangoJSONEncoder()


def round_floats(v):
    return round(v, 2) if isinstance(v, float) else v


def client_metrics(request, pk=None):
    client = get_object_or_404(Client, pk=pk)
    entries = client.entries.order_by('date').values()
    entry_field_names = {
        f.name: ' '.join(
            (f.verbose_name.title(),) + (('({})'.format(f.help_text),) if f.help_text else tuple())
        ) for f in Entry._meta.get_fields() if f.name not in ('id', 'client', 'date', 'notes')
    }
    dates = []
    metrics = {}
    for e in entries:
        d = e['date']
        dates.append(d)
        for m in entry_field_names:
            metric_data = metrics.setdefault(m, {})
            metric_data[d] = e[m]

        metrics.setdefault('Body Fat (lb)', {})[d] = proportion(e['weight'], e['body_fat'])
        metrics.setdefault('Skeletal Muscle (lb)', {})[d] = proportion(
            e['weight'], e['skeletal_muscle']
        )
        weight_in_kg = to_kg(e['weight'])
        metrics.setdefault('Weight (kg)', {})[d] = weight_in_kg
        metrics.setdefault('Ideal Daily Protein Intake (g)', {})[d] = ideal_protein(weight_in_kg)
        height_in_cm = to_cm(client.height)
        bmr = basal_metabolic_rate(weight_in_kg, height_in_cm, client.age, client.sex)
        metrics.setdefault('Basal Metabolic Rate (kcal)', {})[d] = bmr
        metrics.setdefault('Actual vs Ideal Weight (%)', {})[d] = comparison_percentage(
            e['weight'], client.ideal_weight
        )
        tef = thermic_effect_of_food(bmr)
        metrics.setdefault('Thermic Effect of Food (kcal)', {})[d] = tef
        try:
            bmr_mult = get_bmr_multiple(e['activity_rating'])
        except ValueError:
            continue

        tea = thermic_effect_of_activity(bmr, bmr_mult)
        metrics.setdefault('Thermic Effect of Activity (kcal)', {})[d] = tea
        tee = total_energy_expenditure(bmr, tea, tef)
        metrics.setdefault('Total Energy Expenditure (kcal)', {})[d] = tee

    context = {
        'client': client,
        'data': json_encoder.encode([['dates'] + dates] + [
            [entry_field_names.get(m, m)] +
            list(map(round_floats, (metrics[m].get(d) for d in dates))) for m in metrics
        ])
    }

    return render(request, 'client_metrics.html', context=context)
