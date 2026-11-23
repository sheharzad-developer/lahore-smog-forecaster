
import { useCallback, useEffect, useState } from "react";
import { Wind, MapPin, Wifi, WifiOff } from "lucide-react";

import StatCard from "../components/StatCard";
import AirQualityChart from "../components/AirQualityChart";
import api, { getApiErrorMessage } from "../services/api";
import ErrorMessage from "../components/ErrorMessage";

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

  const loadSummary = useCallback(() => {
    setLoading(true);
    setError(null);

    api
      .get<DashboardSummary>("/api/summary")
      .then((response) => {
        setSummary(response.data);
      })
      .catch((err) => {
        console.error("Summary API error:", err);
        setError(getApiErrorMessage(err));
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  if (loading) {
    return <div className="overview">Loading dashboard statistics...</div>;
  }

  if (error) {
    return (
      <div className="overview">
        <ErrorMessage message={error} onRetry={loadSummary} />
      </div>
    );
  }

  if (!summary) {
    return <div className="overview">No dashboard data available.</div>;
  }

  return (
    <div className="overview">
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
    </div>
  );
};

export default Overview;
