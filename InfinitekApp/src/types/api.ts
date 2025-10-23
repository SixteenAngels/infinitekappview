// Backend API Types

export type TokenResponse = {
  access_token: string;
  token_type: 'bearer';
};

export type UserPublic = {
  id: string;
  email: string;
};

export type Device = {
  id: number;
  device_id: string;
  name: string;
  group?: string | null;
};

export type DeviceCreate = {
  name: string;
  device_id: string;
  group?: string | null;
};

export type Measurement = {
  id: number;
  device_id: string;
  sensor: string;
  value: number;
  unit?: string | null;
  created_at: string; // ISO
};

export type Rule = {
  id: number;
  owner_id: string;
  name: string;
  conditions: string; // JSON string
  actions: string; // JSON string
  enabled: boolean;
};

export type DeviceConfig = {
  id: number;
  name: string;
  group?: string | null;
};
