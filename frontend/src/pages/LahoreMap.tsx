import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import api from "../services/api";
import type { Station } from "../types/station";
import "leaflet/dist/leaflet.css";

const LahoreMap = () => {
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get("/api/stations")
      .then((response) => {
        setStations(response.data.stations);
      })
      .catch((err) => {
        setError("Failed to load map stations.");
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="map-page">Loading map stations...</div>;
  }

  if (error) {
    return <div className="map-page">{error}</div>;
  }
  return (
    <div className="map-page">
      <h2>Lahore Air Quality Map</h2>
      <p>Illustrative monitoring station locations and readings</p>

      <div className="map-container">
        <MapContainer
          center={[31.5204, 74.3587]}
          zoom={11}
          scrollWheelZoom={true}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {stations.map((station) => (
            <CircleMarker
              key={station.id}
              center={[station.lat, station.lng]}
              radius={10}
              pathOptions={{
                color: "#ffffff",
                fillColor:
                  station.status === "Offline"
                    ? "#6b7280"
                    : station.pm25 <= 15
                      ? "#16a34a"
                      : station.pm25 <= 35
                        ? "#d97706"
                        : station.pm25 <= 55
                          ? "#ea580c"
                          : "#dc2626",
                fillOpacity: 0.85,
                weight: 2,
              }}
            >
              <Popup>
                <strong>{station.name}</strong>
                <br />
                Neighbourhood: {station.neighbourhood}
                <br />
                PM2.5: {station.pm25} µg/m³
                <br />
                Status: {station.status}
                <br />
                Demonstration data
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      <div className="map-legend">
        <h3>Map Legend</h3>

        <div className="map-legend-items">
          <span>
            <i className="legend-color green" /> Good
          </span>
          <span>
            <i className="legend-color amber" /> Moderate
          </span>
          <span>
            <i className="legend-color orange" /> Unhealthy
          </span>
          <span>
            <i className="legend-color red" /> High PM2.5
          </span>
          <span>
            <i className="legend-color grey" /> Offline
          </span>
        </div>
      </div>
    </div>
  );
};

export default LahoreMap;
