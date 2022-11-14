from enum import Enum
from django.db.models import Q

from django.core import serializers

from candidate.models import Resume


class SelectedDB(Enum):
    SqlLite = ("django.db.backends.sqlite3", 'ORM Queryset')
    PostgreSql = ("django.db.backends.postgresql_psycopg2", 'ORM Queryset')

    @staticmethod
    def get_values():
        return {x.value[0]: x.value[1] for x in SelectedDB}


def raw_query(query_conditions):
    query = "select * from Resume where {}".format(query_conditions)
    return query


def orm_query(query_conditions):
    query = Resume.objects.filter(query_conditions)
    query = serializers.serialize('json', query)
    return query


db_query_generator = {
    "ORM Queryset": orm_query,
    "Raw SQL": raw_query
}
