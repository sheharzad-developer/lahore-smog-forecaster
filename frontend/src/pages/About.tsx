
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
          <li>Develop machine learning models to forecast future air quality.</li>
        </ul>
      </section>

      <section>
        <h3>Technology Stack</h3>
        <div className="technology-list">
          <span>React</span>
          <span>TypeScript</span>
          <span>FastAPI</span>
          <span>PostgreSQL</span>
          <span>Python</span>
          <span>Recharts</span>
          <span>Leaflet</span>
        </div>
      </section>

      <section>
        <h3>Current Development Status</h3>
        <p>
          The full-stack monitoring application is implemented
          with a React frontend, FastAPI backend, and PostgreSQL
          database. Machine learning forecasting and automated
          data integration are planned for future development.
        </p>
      </section>

      <section>
        <h3>Data Information</h3>
        <p>
          The current application uses illustrative sample
          data for demonstration purposes. It does not
          display live environmental measurements or actual
          historical pollution records.
        </p>
      </section>
    </div>
  );
};

export default About;
