import { Routes, Route, Outlet } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import Overview from "./pages/Overview";
import Monitoring from "./pages/Monitoring";
import LahoreMap from "./pages/LahoreMap";
import History from "./pages/History";
import About from "./pages/About";

import "./App.css";

const AppLayout = () => {
  return (
    <div className="app-container">
      <Sidebar />

      <main className="main-content">
        <Header />
        <Outlet />
      </main>
    </div>
  );
};

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Overview />} />

        <Route path="/history" element={<History />} />

        <Route path="/about" element={<About />} />
        
        <Route path="/monitoring" element={<Monitoring />} />

        <Route path="/map" element={<LahoreMap />} />

       
      </Route>
    </Routes>
  );
}

export default App;
