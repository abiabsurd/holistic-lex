from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render


from biometrics.biometrics import (
    get_bmr_multiple, ideal_protein, to_kg, to_cm, basal_metabolic_rate,
    comparison_percentage, thermic_effect_of_activity, thermic_effect_of_food,
    total_energy_expenditure, proportion
)
from biometrics.models import Client, Entry

json_encoder = DjangoJSONEncoder()


def skip_on_error(lambda_calling_func):
    try:
        return lambda_calling_func()
    except Exception:
        return None


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

        metrics.setdefault('Body Fat (lb)', {})[d] = skip_on_error(
            lambda: proportion(e['weight'], e['body_fat'])
        )
        metrics.setdefault('Skeletal Muscle (lb)', {})[d] = skip_on_error(
            lambda: proportion(e['weight'], e['skeletal_muscle'])
        )
        weight_in_kg = skip_on_error(
            lambda: to_kg(e['weight'])
        )
        metrics.setdefault('Weight (kg)', {})[d] = weight_in_kg
        metrics.setdefault('Ideal Daily Protein Intake (g)', {})[d] = skip_on_error(
            lambda: ideal_protein(weight_in_kg)
        )
        height_in_cm = skip_on_error(
            lambda: to_cm(client.height)
        )
        bmr = skip_on_error(
            lambda: basal_metabolic_rate(weight_in_kg, height_in_cm, client.age, client.sex)
        )
        metrics.setdefault('Basal Metabolic Rate (kcal)', {})[d] = bmr
        metrics.setdefault('Actual vs Ideal Weight (%)', {})[d] = skip_on_error(
            lambda: comparison_percentage(e['weight'], client.ideal_weight)
        )
        tef = skip_on_error(
            lambda: thermic_effect_of_food(bmr)
        )
        metrics.setdefault('Thermic Effect of Food (kcal)', {})[d] = tef

        bmr_mult = skip_on_error(
            lambda: get_bmr_multiple(e['activity_rating'])
        )
        tea = skip_on_error(
            lambda: thermic_effect_of_activity(bmr, bmr_mult)
        )
        metrics.setdefault('Thermic Effect of Activity (kcal)', {})[d] = tea
        tee = skip_on_error(
            lambda: total_energy_expenditure(bmr, tea, tef)
        )
        metrics.setdefault('Total Energy Expenditure (kcal)', {})[d] = tee

    # map metrics to x-axis values (dates) for each metric for c3js
    metrics_to_x_axis_names = {}

    # create x-axis values corresponding to each metric's values
    date_cols = []
    metric_cols = []
    for i, m in enumerate(metrics):
        m_name = entry_field_names.get(m, m)
        x_axis = 'x{}'.format(i + 1)
        metrics_to_x_axis_names[m_name] = x_axis
        m_dates = [x_axis]
        m_vals = [m_name]
        for d in dates:
            v = metrics[m].get(d)
            if v is not None:
                m_dates.append(d)
                m_vals.append(v)

        date_cols.append(m_dates)
        metric_cols.append(m_vals)

    print(metrics_to_x_axis_names)
    print(date_cols)
    print(metric_cols)

    context = {
        'client': client,
        'c3': {
            'showOnLoad': metric_cols[0][0],
            'xs': json_encoder.encode(metrics_to_x_axis_names),
            'columns': json_encoder.encode(date_cols + metric_cols)
            # 'columns': json_encoder.encode([['dates'] + dates] + [
            #     [entry_field_names.get(m, m)] +
            #     list(map(round_floats, (metrics[m].get(d) for d in dates))) for m in metrics
            # ])
        }
    }

    return render(request, 'client_metrics.html', context=context)
