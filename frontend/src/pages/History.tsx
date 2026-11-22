
import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import api from "../services/api";

interface HistoryReading {
  day: string;
  pm25: number;
}

type TimeRange = "weekly" | "monthly" | "yearly";

const History = () => {
  const [range, setRange] = useState<TimeRange>("weekly");
  const [chartData, setChartData] = useState<HistoryReading[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    api
      .get(`/api/history/${range}`)
      .then((response) => {
        setChartData(response.data.readings);
      })
      .catch((err) => {
        console.error("History API error:", err);
        setError("Failed to load historical data.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [range]);

  const averagePM25 = chartData.length
    ? Math.round(
        chartData.reduce((total, item) => total + item.pm25, 0) /
          chartData.length
      )
    : 0;

  const highestPM25 = chartData.length
    ? Math.max(...chartData.map((item) => item.pm25))
    : 0;

  const lowestPM25 = chartData.length
    ? Math.min(...chartData.map((item) => item.pm25))
    : 0;

  const exportCSV = () => {
    const csvContent = [
      ["Period", "PM2.5 (µg/m³)"],
      ...chartData.map((item) => [item.day, item.pm25]),
    ]
      .map((row) => row.join(","))
      .join("\n");

    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `lahore-pm25-${range}.csv`;
    link.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="history-page">
      <h2>Historical Air Quality</h2>
      <p>Explore historical PM2.5 trends in Lahore.</p>

      <div className="history-controls">
        <label htmlFor="history-range">Time range:</label>

        <select
          id="history-range"
          value={range}
          onChange={(event) =>
            setRange(event.target.value as TimeRange)
          }
        >
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      {loading && <p>Loading historical data...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && (
        <>
          <button className="export-button" onClick={exportCSV}>
            Export CSV
          </button>

          <div className="history-stats">
            <div className="history-stat-card">
              <h3>Average PM2.5</h3>
              <strong>{averagePM25}</strong>
              <span>µg/m³</span>
            </div>

            <div className="history-stat-card">
              <h3>Highest PM2.5</h3>
              <strong>{highestPM25}</strong>
              <span>µg/m³</span>
            </div>

            <div className="history-stat-card">
              <h3>Lowest PM2.5</h3>
              <strong>{lowestPM25}</strong>
              <span>µg/m³</span>
            </div>
          </div>

          <div className="history-chart-card">
            <h3>
              {range.charAt(0).toUpperCase() + range.slice(1)} PM2.5 Trend
            </h3>
            <p>PM2.5 concentration (µg/m³)</p>

            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="pm25"
                  stroke="#2563eb"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="history-table-card">
            <h3>Historical Readings</h3>

            <table className="history-table">
              <thead>
                <tr>
                  <th>Period</th>
                  <th>PM2.5 (µg/m³)</th>
                </tr>
              </thead>

              <tbody>
                {chartData.map((item) => (
                  <tr key={item.day}>
                    <td>{item.day}</td>
                    <td>{item.pm25}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="demo-notice">
            Illustrative data only. These are not actual historical measurements.
          </p>
        </>
      )}
    </div>
  );
};

export default History;
