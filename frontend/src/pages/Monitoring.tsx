import { useCallback, useEffect, useState } from "react";
import StationTable from "../components/StationTable";
import api, { getApiErrorMessage } from "../services/api";
import ErrorMessage from "../components/ErrorMessage";
import type { Station } from "../types/station";

const Monitoring = () => {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");
  const [sortOrder, setSortOrder] = useState("none");
  const [currentPage, setCurrentPage] = useState(1);
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const totalStations = stations.length;

  const onlineStations = stations.filter(
    (station) => station.status === "Online",
  ).length;

  const offlineStations = stations.filter(
    (station) => station.status === "Offline",
  ).length;

  const filteredStations = stations
    .filter((station) => {
      const matchesSearch = `${station.name} ${station.neighbourhood}`
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesStatus = status === "All" || station.status === status;

      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      if (sortOrder === "high") {
        return b.pm25 - a.pm25;
      }

      if (sortOrder === "low") {
        return a.pm25 - b.pm25;
      }

      return 0;
    });

  const stationsPerPage = 3;

  const totalPages = Math.ceil(filteredStations.length / stationsPerPage);

  const startIndex = (currentPage - 1) * stationsPerPage;

  const paginatedStations = filteredStations.slice(
    startIndex,
    startIndex + stationsPerPage,
  );

  const loadStations = useCallback(() => {
    setLoading(true);
    setError(null);

    api
      .get<{ stations: Station[] }>("/api/stations")
      .then((response) => {
        setStations(response.data.stations);
      })
      .catch((err) => {
        console.error("Stations API error:", err);
        setError(getApiErrorMessage(err));
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    loadStations();
  }, [loadStations]);

  if (loading) {
    return <div className="monitoring-page">Loading stations...</div>;
  }

  if (error) {
    return (
      <div className="monitoring-page">
        <ErrorMessage message={error} onRetry={loadStations} />
      </div>
    );
  }

  return (
    <div className="monitoring-page">
      <h2>Live Monitoring Stations</h2>
      <p>Search, filter and sort monitoring stations.</p>

      <div className="station-summary">
        <div>
          <h3>{totalStations}</h3>
          <p>Total Stations</p>
        </div>

        <div>
          <h3>{onlineStations}</h3>
          <p>Online Stations</p>
        </div>

        <div>
          <h3>{offlineStations}</h3>
          <p>Offline Stations</p>
        </div>
      </div>

      <div className="monitoring-controls">
        <input
          type="text"
          className="station-search"
          placeholder="Search stations..."
          aria-label="Search stations"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <select
          className="station-select"
          aria-label="Filter by status"
          value={status}
          onChange={(event) => setStatus(event.target.value)}
        >
          <option value="All">All Stations</option>
          <option value="Online">Online</option>
          <option value="Offline">Offline</option>
        </select>

        <select
          className="station-select"
          aria-label="Sort by PM2.5"
          value={sortOrder}
          onChange={(event) => setSortOrder(event.target.value)}
        >
          <option value="none">Default Order</option>
          <option value="high">Highest PM2.5</option>
          <option value="low">Lowest PM2.5</option>
        </select>
      </div>

      <StationTable stations={paginatedStations} />

      <div className="pagination">
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(currentPage - 1)}
        >
          Previous
        </button>

        <span>
          Page {currentPage} of {Math.max(totalPages, 1)}
        </span>

        <button
          disabled={currentPage >= totalPages}
          onClick={() => setCurrentPage(currentPage + 1)}
        >
          Next
        </button>
      </div>

      <div className="severity-legend">
        <span className="legend-item">
          <span className="legend-dot good-dot" />
          Good
        </span>

        <span className="legend-item">
          <span className="legend-dot moderate-dot" />
          Moderate
        </span>

        <span className="legend-item">
          <span className="legend-dot unhealthy-dot" />
          Unhealthy
        </span>

        <span className="legend-item">
          <span className="legend-dot hazardous-dot" />
          Hazardous
        </span>
      </div>

      <p className="demo-notice">
        Demonstration data only. These are not live readings.
      </p>
    </div>
  );
};

export default Monitoring;
