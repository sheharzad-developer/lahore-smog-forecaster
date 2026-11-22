"""Sample monitoring stations used to seed an empty database."""

SAMPLE_STATIONS = [
    {"name": "Gulberg Station", "neighbourhood": "Gulberg III", "pm25": 185,
     "status": "Online", "lat": 31.5204, "lng": 74.3587},
    {"name": "DHA Station", "neighbourhood": "DHA Phase 5", "pm25": 142,
     "status": "Online", "lat": 31.4697, "lng": 74.4086},
    {"name": "Johar Town Station", "neighbourhood": "Johar Town", "pm25": 210,
     "status": "Online", "lat": 31.4697, "lng": 74.2728},
    {"name": "Model Town Station", "neighbourhood": "Model Town", "pm25": 95,
     "status": "Offline", "lat": 31.4833, "lng": 74.3250},
    {"name": "Walled City Station", "neighbourhood": "Walled City", "pm25": 165,
     "status": "Online", "lat": 31.5820, "lng": 74.3290},
]


SAMPLE_HISTORY = {
    "weekly": [
        ("Mon", 120), ("Tue", 145), ("Wed", 135), ("Thu", 180),
        ("Fri", 165), ("Sat", 190), ("Sun", 185),
    ],
    "monthly": [
        ("Week 1", 110), ("Week 2", 135), ("Week 3", 160), ("Week 4", 145),
    ],
    "yearly": [
        ("Jan", 180), ("Feb", 165), ("Mar", 120), ("Apr", 90),
        ("May", 75), ("Jun", 65), ("Jul", 70), ("Aug", 85),
        ("Sep", 110), ("Oct", 150), ("Nov", 190), ("Dec", 210),
    ],
}
