import os
import folium, pandas
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/map')
    def map():
        dirname = os.path.dirname(__file__)
        stations_path = os.path.join(dirname, 'static/json/stations.json')
        print(stations_path)
        stations = pandas.read_json(stations_path) # http://api.gios.gov.pl/pjp-api/rest/station/findAll
        fg = folium.FeatureGroup(name="airMap")
        cities = list(stations['city'])
        names = list(stations['stationName'])
        lat = list(stations['gegrLat'])
        lon = list(stations['gegrLon'])
        voivodeships_path = os.path.join(dirname, 'static/json/voivodeships.json')
        fg.add_child(folium.GeoJson(data=open(voivodeships_path).read()))
        for c, n, ln, lt in zip(cities, names, lon, lat):
            p = folium.Popup('<b>' + str(c['name']) + '</b><br/>' + str(n) + '<br/>')
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius=5,
            fill=True, fill_opacity=1, popup=p, color='MediumAquaMarine'))
        map = folium.Map(location=[52.0173753,19.6137545], zoom_start=6) #Stamen Toner, Mapbox Bright
        map.add_child(fg)
        map_template = os.path.join(dirname, 'templates/map.html')
        map = map.save(map_template)
        return render_template('map.html')
    return app
