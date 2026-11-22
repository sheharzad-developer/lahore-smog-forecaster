
import type { Station } from "../types/station";

interface StationTableProps {
  stations: Station[];
}

const StationTable = ({ stations }: StationTableProps) => {
  return (
    <div className="table-container">
      <table className="station-table">
        <thead>
          <tr>
            <th>Station</th>
            <th>Neighbourhood</th>
            <th>PM2.5 (µg/m³)</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {stations.map((station) => (
            <tr key={station.id}>
              <td>{station.name}</td>
              <td>{station.neighbourhood}</td>
              <td>
                <span
                  className={`pm25-badge ${
                    station.pm25 <= 15
                      ? "good"
                      : station.pm25 <= 35
                      ? "moderate"
                      : station.pm25 <= 55
                      ? "unhealthy"
                      : "hazardous"
                  }`}
                >
                  {station.pm25} µg/m³
                </span>
              </td>
              <td>
                <span
                  className={
                    station.status === "Online"
                      ? "status-online"
                      : "status-offline"
                  }
                >
                  {station.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {stations.length === 0 && (
        <p className="table-empty">No monitoring stations found.</p>
      )}
    </div>
  );
};

export default StationTable;
