import folium
import pandas

data = pandas.read_csv("Webmap_datasources/Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

fgv.add_child(folium.Marker(location=[38.58, -99.09], popup="Starting Point", icon = folium.Icon(color = "black")))

# for lt, ln, el, nm in zip(lat, lon, elev, name):
#     iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
#     fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_producer(el))))

for lt, ln, el, nm in zip(lat, lon, elev, name):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el) + " m", 
    fill_color = color_producer(el), color='grey', fill_opacity=0.7)) #fill=True ifcolor is invisible

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("Webmap_datasources/world.json", "r", encoding="utf-8-sig").read(), 
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")