import React from 'react';
import { View } from 'react-native';
import { Card, Text, Button } from 'react-native-paper';

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
    <Card style={{ marginBottom: 8 }}>
      <Card.Title title={device.name} subtitle={device.device_id} />
      <Card.Actions>
        <Button onPress={onDashboard}>Dashboard</Button>
        <Button onPress={onSync}>Sync</Button>
      </Card.Actions>
    </Card>
  );
}
