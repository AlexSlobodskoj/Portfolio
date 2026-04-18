{% macro count_by_outcome(outcome_value) %}
    sum(case when outcome = '{{ outcome_value }}' then 1 else 0 end)
{% endmacro %}