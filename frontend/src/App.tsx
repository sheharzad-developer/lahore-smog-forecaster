
import { lazy, Suspense } from "react";
import { Routes, Route, Outlet } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import "./App.css";

// Load pages only when users visit their routes
const Overview = lazy(() => import("./pages/Overview"));
const Monitoring = lazy(() => import("./pages/Monitoring"));
const LahoreMap = lazy(() => import("./pages/LahoreMap"));
const History = lazy(() => import("./pages/History"));
const About = lazy(() => import("./pages/About"));

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
    <Suspense fallback={<div className="page-loading">Loading page...</div>}>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Overview />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/map" element={<LahoreMap />} />
        </Route>
      </Routes>
    </Suspense>
  );
}

export default App;
