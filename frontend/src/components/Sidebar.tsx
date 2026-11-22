
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Map,
  Activity,
  History,
  Info,
} from "lucide-react";

const menuItems = [
  { name: "Overview", path: "/", icon: LayoutDashboard },
  { name: "Live Monitoring", path: "/monitoring", icon: Activity },
  { name: "Lahore Map", path: "/map", icon: Map },
  { name: "Historical Data", path: "/history", icon: History },
  { name: "About", path: "/about", icon: Info },
];

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <h2>Lahore Air</h2>

      <nav>
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              to={item.path}
              key={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
              }
            >
              <Icon size={19} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;
