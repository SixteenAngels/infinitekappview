import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuth } from '../context/AuthContext';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import DevicesScreen from '../screens/DevicesScreen';
import AddDeviceScreen from '../screens/AddDeviceScreen';
import SensorDashboard from '../screens/SensorDashboard';
import RulesBuilder from '../screens/RulesBuilder';
import OTAUpdate from '../screens/OTAUpdate';
import DeviceSync from '../screens/DeviceSync';

export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  Devices: undefined;
  AddDeviceScreen: undefined;
  SensorDashboard: { device_id: string };
  RulesBuilder: undefined;
  OTAUpdate: undefined;
  DeviceSync: { device_id: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  const { user } = useAuth();

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {user ? (
          <>
            <Stack.Screen name="Devices" component={DevicesScreen} />
            <Stack.Screen name="AddDeviceScreen" component={AddDeviceScreen} />
            <Stack.Screen name="SensorDashboard" component={SensorDashboard} />
            <Stack.Screen name="RulesBuilder" component={RulesBuilder} />
            <Stack.Screen name="OTAUpdate" component={OTAUpdate} />
            <Stack.Screen name="DeviceSync" component={DeviceSync} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
