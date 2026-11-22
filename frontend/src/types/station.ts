export interface Station {
  id: number;
  name: string;
  neighbourhood: string;
  pm25: number;
  status: "Online" | "Offline";
  lat: number;
  lng: number;
}
