
import { useCallback, useEffect, useState } from "react";
import { Wind, MapPin, Wifi, WifiOff } from "lucide-react";

import StatCard from "../components/StatCard";
import AirQualityChart from "../components/AirQualityChart";
import api, {
  getApiErrorMessage,
  getForecast,
  type ForecastResponse,
} from "../services/api";
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
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [forecastLoading, setForecastLoading] = useState(true);
  const [forecastError, setForecastError] = useState<string | null>(null);

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

  const loadForecast = useCallback(() => {
    setForecastLoading(true);
    setForecastError(null);

    getForecast()
      .then(setForecast)
      .catch((err) => {
        console.error("Forecast API error:", err);
        setForecastError(getApiErrorMessage(err));
      })
      .finally(() => {
        setForecastLoading(false);
      });
  }, []);

  useEffect(() => {
    loadForecast();
  }, [loadForecast]);

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

      <section className="forecast-section">
        <div className="section-header">
          <div>
            <h2>AI Air Quality Forecast</h2>
            <p>Gulberg III · Experimental ML predictions</p>
          </div>

          <button onClick={loadForecast} disabled={forecastLoading}>
            {forecastLoading ? "Updating..." : "Refresh Forecast"}
          </button>
        </div>

        {forecastLoading && (
          <p>Loading air quality forecast...</p>
        )}

        {forecastError && (
          <ErrorMessage
            message={forecastError}
            onRetry={loadForecast}
          />
        )}

        {forecast && !forecastLoading && (
          <>
            <div className="forecast-current">
              <span>Latest PM2.5 reading</span>
              <strong>
                {forecast.current_pm25.toFixed(2)} {forecast.unit}
              </strong>
              <small>
                Updated: {new Date(forecast.latest_reading).toLocaleString()}
              </small>
            </div>

            <div className="forecast-grid">
              <div className="forecast-card">
                <span>Next 24 Hours</span>
                <strong>{forecast.forecasts["24h"].toFixed(2)}</strong>
                <small>µg/m³</small>
              </div>

              <div className="forecast-card">
                <span>Next 48 Hours</span>
                <strong>{forecast.forecasts["48h"].toFixed(2)}</strong>
                <small>µg/m³</small>
              </div>

              <div className="forecast-card">
                <span>Next 72 Hours</span>
                <strong>{forecast.forecasts["72h"].toFixed(2)}</strong>
                <small>µg/m³</small>
              </div>
            </div>
          </>
        )}

        <p className="forecast-disclaimer">
          Experimental ML forecasts based on one monitoring sensor in Gulberg
          III. Predictions are not citywide measurements or official health
          advisories.
        </p>
      </section>

      <AirQualityChart />
    </div>
  );
};

export default Overview;
