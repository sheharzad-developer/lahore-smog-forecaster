
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  unit: string;
  icon: LucideIcon;
  description: string;
}

const StatCard = ({
  title,
  value,
  unit,
  icon: Icon,
  description,
}: StatCardProps) => {
  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <span>{title}</span>
        <Icon size={22} />
      </div>

      <div className="stat-value">
        {value}
        <small>{unit}</small>
      </div>

      <p>{description}</p>
    </div>
  );
};

export default StatCard;
