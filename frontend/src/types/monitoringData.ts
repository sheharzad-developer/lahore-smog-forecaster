import type { Station } from "./station";

export const stations: Station[] = [
  {
    id: 1,
    name: "Gulberg Station",
    neighbourhood: "Gulberg III",
    pm25: 185,
    status: "Online",
    lat: 31.5204,
    lng: 74.3587,
  },
  {
    id: 2,
    name: "DHA Station",
    neighbourhood: "DHA Phase 5",
    pm25: 142,
    status: "Online",
    lat: 31.4697,
    lng: 74.4086,
  },
  {
    id: 3,
    name: "Johar Town Station",
    neighbourhood: "Johar Town",
    pm25: 210,
    status: "Online",
    lat: 31.4697,
    lng: 74.2728,
  },
  {
    id: 4,
    name: "Model Town Station",
    neighbourhood: "Model Town",
    pm25: 95,
    status: "Offline",
    lat: 31.4833,
    lng: 74.3250,
  },
  {
    id: 5,
    name: "Walled City Station",
    neighbourhood: "Walled City",
    pm25: 165,
    status: "Online",
    lat: 31.582,
    lng: 74.3290,
  },
];
