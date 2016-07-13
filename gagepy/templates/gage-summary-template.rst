{{ gage_name }}
{{ "=" * (gage_name|length) }}

Parameters
----------
{% for i in range(parameters|length) %}
{{ i + 1 }}. {{ parameters[i].name }} ({{ parameters[i].units }})
{% endfor %}

{% for parameter in parameters %}
{{ parameter.name }} ({{ parameter.units }})
{{ "-" * (parameter.name|length + parameter.units|length + 3) }}

Parameter Info
~~~~~~~~~~~~~~
Start date:    {{ parameter.dates[0] }}
End date:      {{ parameter.dates[-1] }}
Total values:  {{ parameter.values|length }}

Quick Stats
~~~~~~~~~~~
Max:    {{ '{0:0.2f}'.format(parameter.max) }}    {{ parameter.max_date }}
Min:    {{ '{0:0.2f}'.format(parameter.min) }}    {{ parameter.min_date }}
Mean:   {{ '{0:0.2f}'.format(parameter.mean) }}

{% endfor %}
