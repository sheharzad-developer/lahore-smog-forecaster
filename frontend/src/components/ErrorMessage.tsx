import { AlertTriangle, RotateCw } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

const ErrorMessage = ({ message, onRetry }: ErrorMessageProps) => {
  return (
    <div className="error-message" role="alert">
      <AlertTriangle size={20} aria-hidden="true" />

      <p>{message}</p>

      {onRetry && (
        <button type="button" className="retry-button" onClick={onRetry}>
          <RotateCw size={15} aria-hidden="true" />
          Retry
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
