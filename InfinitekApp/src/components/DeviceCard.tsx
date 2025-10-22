import React from 'react';
import { View, Text, Button } from 'react-native';

export type Device = {
  id: number;
  device_id: string;
  name: string;
  group?: string | null;
};

export default function DeviceCard({ device, onDashboard, onSync }: {
  device: Device,
  onDashboard: () => void,
  onSync: () => void,
}) {
  return (
    <View style={{ padding: 12, backgroundColor: '#eee', borderRadius: 8, marginBottom: 8 }}>
      <Text style={{ fontWeight: 'bold' }}>{device.name}</Text>
      <Text style={{ color: '#555' }}>{device.device_id}</Text>
      <View style={{ flexDirection: 'row', gap: 8, marginTop: 8 }}>
        <Button title="Dashboard" onPress={onDashboard} />
        <Button title="Sync" onPress={onSync} />
      </View>
    </View>
  );
}
