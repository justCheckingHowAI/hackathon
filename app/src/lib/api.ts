const fallbackApiUrl =
  typeof window === "undefined"
    ? "http://127.0.0.1:8001"
    : `${window.location.protocol}//${window.location.hostname}:8001`;

export const API_URL = import.meta.env.VITE_API_URL ?? fallbackApiUrl;
