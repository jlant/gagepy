{{ name }} ({{ units }})
{{ "-" * (name|length + units|length + 3) }}

Parameter Info
~~~~~~~~~~~~~~
Start date    {{ start_date }}
End date      {{ end_date }}
No. values    {{ num_vals}}


Quick Stats
~~~~~~~~~~~
Max    {{ '{0:0.2f}'.format(max) }}    {{ max_date }}
Min    {{ '{0:0.2f}'.format(min) }}    {{ min_date }}
Mean   {{ '{0:0.2f}'.format(mean) }}
