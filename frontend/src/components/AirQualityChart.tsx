
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const pollutionData = [
  { day: "Mon", pm25: 120 },
  { day: "Tue", pm25: 145 },
  { day: "Wed", pm25: 135 },
  { day: "Thu", pm25: 180 },
  { day: "Fri", pm25: 165 },
  { day: "Sat", pm25: 190 },
  { day: "Sun", pm25: 185 },
];

const AirQualityChart = () => {
  return (
    <div className="chart-card">
      <h2>PM2.5 Historical Trend</h2>
      <p>Last 7 days (illustrative data)</p>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={pollutionData}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="day" />

          <YAxis
            label={{
              value: "PM2.5 (µg/m³)",
              angle: -90,
              position: "insideLeft",
            }}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="pm25"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AirQualityChart;
