import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// Centralized API response error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);

    return Promise.reject(error);
  }
);

// Convert API errors into user-friendly messages
export function getApiErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return "Something went wrong. Please try again.";
  }

  // Request timeout
  if (
    error.code === "ECONNABORTED" ||
    error.code === "ETIMEDOUT"
  ) {
    return "The server took too long to respond. Please try again.";
  }

  // Backend unavailable or network error
  if (!error.response) {
    return "Can't reach the server. Make sure the backend is running.";
  }

  // Get error detail from FastAPI
  const detail = (error.response.data as { detail?: unknown })?.detail;

  if (typeof detail === "string" && detail) {
    return detail;
  }

  // Handle HTTP status codes
  switch (error.response.status) {
    case 400:
      return "Invalid request. Please check your input.";

    case 404:
      return "The requested resource was not found.";

    case 500:
      return "Internal server error. Please try again later.";

    case 503:
      return "The service is temporarily unavailable.";

    default:
      return `Request failed (${error.response.status}). Please try again.`;
  }
}

export default api;