
import { useEffect, useState } from "react";
import { Wind, MapPin, Wifi, WifiOff } from "lucide-react";

import StatCard from "../components/StatCard";
import AirQualityChart from "../components/AirQualityChart";
import api from "../services/api";

interface DashboardSummary {
  data_type: string;
  total_stations: number;
  online_stations: number;
  offline_stations: number;
  average_pm25: number;
}

const Overview = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get("/api/summary")
      .then((response) => {
        setSummary(response.data);
      })
      .catch((error) => {
        console.error("Summary API error:", error);
        setError("Failed to load dashboard statistics.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="overview">
      {loading && <p>Loading dashboard statistics...</p>}

      {error && <p>{error}</p>}

      {summary && (
        <>
          <div className="stats-grid">
            <StatCard
              title="Average PM2.5"
              value={String(summary.average_pm25)}
              unit="µg/m³"
              icon={Wind}
              description="Sample station average"
            />

            <StatCard
              title="Total Stations"
              value={String(summary.total_stations)}
              unit="stations"
              icon={MapPin}
              description="All demonstration stations"
            />

            <StatCard
              title="Online Stations"
              value={String(summary.online_stations)}
              unit="stations"
              icon={Wifi}
              description="Currently marked online"
            />

            <StatCard
              title="Offline Stations"
              value={String(summary.offline_stations)}
              unit="stations"
              icon={WifiOff}
              description="Currently marked offline"
            />
          </div>

          <AirQualityChart />
        </>
      )}
    </div>
  );
};

export default Overview;
