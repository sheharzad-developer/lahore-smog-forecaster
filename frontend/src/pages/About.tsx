
const About = () => {
  return (
    <div className="about-page">
      <h2>About Lahore Smog Forecaster</h2>

      <p className="about-intro">
        Lahore Smog Forecaster is an air quality monitoring
        and forecasting project designed to help users
        understand pollution trends across Lahore.
      </p>

      <section>
        <h3>Project Objectives</h3>
        <ul>
          <li>Monitor PM2.5 pollution levels.</li>
          <li>Visualize air quality across Lahore.</li>
          <li>Explore historical pollution trends.</li>
          <li>Eventually forecast future air quality.</li>
        </ul>
      </section>

      <section>
        <h3>Technology Stack</h3>
        <div className="technology-list">
          <span>React</span>
          <span>TypeScript</span>
          <span>FastAPI (planned)</span>
          <span>PostgreSQL (planned)</span>
          <span>Recharts</span>
          <span>Leaflet</span>
        </div>
      </section>

      <section>
        <h3>Data Information</h3>
        <p>
          The current application uses illustrative sample
          data for demonstration purposes. It does not
          display live environmental measurements.
        </p>
      </section>
    </div>
  );
};

export default About;
