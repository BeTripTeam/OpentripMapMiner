from typing import List
import requests
from models.Point import Point
from models.PostCluster import PostCluster


class PlacesMiner:
    base_url = "https://api.opentripmap.com/0.1/en/places"
    api_key  = "5ae2e3f221c38a28845f05b696b783ac144a4bb9b80ddb05ee4f0b7a"
    
    def get_paces_near(self, point: Point) -> List[PostCluster]:
        lat_min, lat_max, lon_min, lon_max = self.mk_cell(point)
        
        res = []
        
        places = self.get_places(lat_min, lat_max, lon_min, lon_max)
        for place in places:
            if place.get('properties').get('name'):
                p = self.get_place_info(place.get('properties').get('xid'))
                pc = PostCluster(Point(p.get('point', {}).get('lat'), p.get('point', {}).get('lon')), [])
                pc.set_category(p.get("kinds", ""))
                pc.name = p.get("name")
                pc.descr = [p.get('info', {}).get('descr', '')]
                pc.image_url = p.get('image', '')
                res.append(pc)
        return res

    def mk_cell(self, p: Point, r=20):
        deg_per_km = 0.0089932036372453797
        r_rad = deg_per_km * r
        return p.latitude - r_rad, p.latitude + r_rad, p.longitude - r_rad, p.longitude + r_rad

    def mk_point(self, place):
        pass

    def get_places(self, lat_min, lat_max, lon_min, lon_max):
        """
        Response body:
                {
                  "type": "FeatureCollection",
                  "features": [
                    {
                      "type": "Feature",
                      "id": 2290043,
                      "geometry": {
                        "type": "Point",
                        "coordinates": [
                          29.984394,
                          60.007336
                        ]
                      },
                      "properties": {
                        "xid": "W249976250",
                        "rate": 0,
                        "name": "",
                        "osm": "way/249976250",
                        "kinds": "interesting_places,natural,beaches,other_beaches"
                      }
                    },
                    ...]
        """
        url = self.base_url + \
              f"/bbox" \
              f"?lon_min={lon_min}" \
              f"&lon_max={lon_max}" \
              f"&lat_min={lat_min}" \
              f"&lat_max={lat_max}" \
              f"&apikey={self.api_key}"
        res = requests.get(url).json().get('features')
        return res
        
    def get_place_info(self, xid: str):
        """
        Response body:
            {
              "preview": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Mikhaylovsky_garden,_Saint_Petersburg.jpg/400px-Mikhaylovsky_garden,_Saint_Petersburg.jpg",
              "image": "https://commons.wikimedia.org/wiki/File:Mikhaylovsky%20garden%2C%20Saint%20Petersburg.jpg",
              "sources": {
                "geometry": "osm",
                "attributes": [
                  "osm",
                  "wikidata"
                ]
              },
              "bbox": {
                "lat_max": 59.941334,
                "lat_min": 59.938278,
                "lon_max": 30.336556,
                "lon_min": 30.328612
              },
              "osm": "relation/2614476",
              "otm": "https://opentripmap.com/en/card/R2614476",
              "kinds": "cultural,urban_environment,gardens_and_parks,interesting_places",
              "point": {
                "lon": 30.332874,
                "lat": 59.939827
              },
              "xid": "R2614476",
              "rate": "3h",
              "name": "Mikhailovsky garden",
              "wikipedia": "https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D1%81%D0%B0%D0%B4",
              "wikidata": "Q4297751"
            }
        """
        url = self.base_url + \
              f"/xid" \
              f"/{xid}" \
              f"?apikey={self.api_key}"
        res = requests.get(url).json()
        return res
    

pm = PlacesMiner()
places = pm.get_paces_near(Point(59.9390095,29.5303098))
print(places)