import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import api from '../api/api';

export type AuthContextType = {
  user: { email: string } | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [user, setUser] = useState<{ email: string } | null>(null);

  useEffect(() => {
    (async () => {
      const token = (await SecureStore.getItemAsync('jwt_token')) || (await AsyncStorage.getItem('jwt_token'));
      const email = await AsyncStorage.getItem('user_email');
      if (token && email) setUser({ email });
    })();
  }, []);

  const login = async (email: string, password: string) => {
    // FastAPI login uses OAuth2PasswordRequestForm fields: username, password
    const form = new FormData();
    form.append('username', email);
    form.append('password', password);
    const res = await api.post('/auth/login', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    const token = (res.data as any).access_token as string;
    await SecureStore.setItemAsync('jwt_token', token);
    await AsyncStorage.setItem('user_email', email);
    setUser({ email });
  };

  const register = async (email: string, password: string) => {
    await api.post('/auth/register', { email, password });
    await login(email, password);
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync('jwt_token');
    await AsyncStorage.multiRemove(['user_email']);
    setUser(null);
  };

  const value = useMemo(() => ({ user, login, register, logout }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
