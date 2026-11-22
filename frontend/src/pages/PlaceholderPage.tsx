
interface PlaceholderPageProps {
  title: string;
  description: string;
}

const PlaceholderPage = ({
  title,
  description,
}: PlaceholderPageProps) => {
  return (
    <div className="placeholder-page">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
};

export default PlaceholderPage;
