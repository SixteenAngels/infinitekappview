import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { AuthProvider } from './src/context/AuthContext';
import AppNavigator from './src/navigation/AppNavigator';
import { MD3DarkTheme, MD3LightTheme, PaperProvider } from 'react-native-paper';
import { useColorScheme } from 'react-native';

export default function App() {
  const scheme = useColorScheme();
  const theme = scheme === 'dark' ? MD3DarkTheme : MD3LightTheme;
  return (
    <PaperProvider theme={theme}>
      <AuthProvider>
        <StatusBar style="auto" />
        <AppNavigator />
      </AuthProvider>
    </PaperProvider>
  );
}
