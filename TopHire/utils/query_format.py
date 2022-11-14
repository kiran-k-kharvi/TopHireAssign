from django.db.models import Q


def combine_condition(sub_condition, logical_operator, field_name, keyword):
    field_name = field_name + "__icontains"
    keyword = keyword if isinstance(keyword, Q) else Q(**{field_name: keyword})
    if sub_condition:
        if logical_operator == 'AND':
            sub_condition.add(keyword, Q.AND)
        else:
            sub_condition.add(keyword, Q.OR)
    else:
        sub_condition = keyword
    return sub_condition


def orm(keywords, field_name):
    sub_condition = Q()
    logical_operator = ''
    for each in keywords:
        if isinstance(each, Q):
            sub_condition = combine_condition(sub_condition, logical_operator, field_name, each)
        elif each in {"AND", "OR"}:
            logical_operator = 'AND' if each == 'AND' else ' OR'
        else:
            sub_condition = combine_condition(sub_condition, logical_operator, field_name, each)
    return sub_condition


def raw_sql(keywords, field_name):
    condition_builder = 'CHARINDEX({0},{1}) > 0'
    sub_condition = ''
    for each in keywords:
        if field_name in each:
            sub_condition += each
        elif each in {"AND", "OR"}:
            sub_condition += " " + each + " "
        else:
            sub_condition += condition_builder.format(each, field_name)
    return '(' + sub_condition + ')'


query_format = {
    'ORM Queryset': orm,
    'Raw SQL': raw_sql
}
