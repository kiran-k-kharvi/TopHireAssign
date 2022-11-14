import json
from django.db import connection
from django.views import View

from utils.enums import SelectedDB
from utils.helpers import validate_and_parse_query
from django.shortcuts import HttpResponse
from utils.queryGenarotor import generate_db_query


class CustomQueryView(View):

    def get(self, request):
        query = json.loads(request.body).get('query')
        field_name = 'text'
        is_validated = validate_and_parse_query(query=query)

        if is_validated:
            db_name = connection.settings_dict['ENGINE']
            db_types = SelectedDB.get_values()
            if db_name in db_types:
                output_format = db_types.get(db_name)
                generated_query = generate_db_query(query=query, output_format='Raw SQL', field_name=field_name)
                print(generated_query)
            else:
                return HttpResponse(json.dumps({'error': 'no db format mapped'}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error': 'Invalid query'}),
                                content_type="application/json")
        result = {'query': generated_query}
        result = json.dumps(result)
        return HttpResponse(result)
