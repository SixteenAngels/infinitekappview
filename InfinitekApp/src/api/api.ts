import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import type { Device, DeviceCreate, Measurement, Rule, TokenResponse, UserPublic, DeviceConfig } from '../types/api';

const FALLBACK_BASE = Platform.OS === 'android' ? 'http://10.0.2.2:8000/api' : 'http://127.0.0.1:8000/api';
export const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? FALLBACK_BASE;

const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
});

api.interceptors.request.use(async (config) => {
  const token = (await SecureStore.getItemAsync('jwt_token')) || (await AsyncStorage.getItem('jwt_token'));
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

// Convenience typed helpers
export const AuthAPI = {
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const form = new FormData();
    form.append('username', email);
    form.append('password', password);
    const res = await api.post<TokenResponse>('/auth/login', form, { headers: { 'Content-Type': 'multipart/form-data' } });
    return res.data;
  },
  register: async (email: string, password: string): Promise<UserPublic> => {
    const res = await api.post<UserPublic>('/auth/register', { email, password });
    return res.data;
  },
};

export const DevicesAPI = {
  list: async (): Promise<Device[]> => (await api.get<Device[]>('/devices/')).data,
  create: async (payload: DeviceCreate): Promise<Device> => (await api.post<Device>('/devices/', payload)).data,
  update: async (id: number, payload: Partial<Pick<Device, 'name' | 'group'>>): Promise<Device> =>
    (await api.patch<Device>(`/devices/${id}`, payload)).data,
  getConfig: async (id: number): Promise<DeviceConfig> => (await api.get<DeviceConfig>(`/devices/${id}/config`)).data,
  putConfig: async (id: number, payload: Partial<Pick<Device, 'name' | 'group'>>): Promise<DeviceConfig> =>
    (await api.put<DeviceConfig>(`/devices/${id}/config`, payload)).data,
};

export const MeasurementsAPI = {
  list: async (params: { device_id?: string; sensor?: string; limit?: number } = {}): Promise<Measurement[]> =>
    (await api.get<Measurement[]>('/measurements', { params })).data,
};

export const RulesAPI = {
  list: async (): Promise<Rule[]> => (await api.get<Rule[]>('/rules')).data,
  create: async (payload: Pick<Rule, 'name' | 'conditions' | 'actions'>): Promise<Rule> =>
    (await api.post<Rule>('/rules', payload)).data,
};
