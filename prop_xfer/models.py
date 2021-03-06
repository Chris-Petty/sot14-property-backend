from dateutil.relativedelta import relativedelta
from flask.ext.sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping


db = SQLAlchemy()


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_no = db.Column(db.String(100))
    location = db.Column(Geometry('POINT', srid=4326))
    action = db.Column(db.String(10))  # new or existing
    week_start = db.Column(db.Date(), index=True)

    def __init__(self, title_no, location, action, week_start):
        self.title_no = title_no
        self.location = location
        self.action = action
        self.week_start = week_start

    def __repr__(self):
        return '<Transfer %d:%s>' % (self.id, self.title_no)

    @property
    def week_end(self):
        return self.week_start + relativedelta(weeks=1)

    def as_geojson(self):
        """ Return the transfer as a GeoJSON Feature """
        return {
            "type": "Feature",
            "geometry": mapping(to_shape(self.location)),
            "properties": {
                "action": self.action,
            }
        }
