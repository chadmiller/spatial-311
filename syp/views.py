
import psycopg2
from itertools import groupby

from django.shortcuts import render
from django.http import JsonResponse

db_name = "spatial-info"

def front(request):
    return render(request, "front.html")

def api_get_point_info(request):
    lng = float(request.GET["lng"])  # cleanses input
    lat = float(request.GET["lat"])  # cleanses input

    with psycopg2.connect("dbname='{}'".format(db_name)) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT topic.name, parcel_tags.id, parcel_tags.key, parcel_tags.value, parcel_tags.make_visible AND parcel_tags.value IS NOT NULL FROM parcel_tags LEFT JOIN parcel on (parcel_tags.parcel=parcel.id) LEFT JOIN import ON (parcel.import=import.id) LEFT JOIN topic on (topic.id=import.topic) WHERE ST_Contains(parcel.shape, ST_MakePoint({},{})) ORDER BY topic.name, parcel.id, parcel_tags.ordering, parcel_tags.key;".format(lng, lat))
            return JsonResponse({ "data": [(k, list(v)) for k, v in groupby(cur.fetchall(), key=lambda trio: trio[0])] })
