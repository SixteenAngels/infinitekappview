import React, { useEffect, useState } from 'react';
import { View, Alert } from 'react-native';
import { Text, TextInput, Button } from 'react-native-paper';
import api from '../api/api';

export default function DeviceSync({ route }: any) {
  const { device_id } = route.params as { device_id: string };
  const [name, setName] = useState('');
  const [group, setGroup] = useState('');
  const [devicePk, setDevicePk] = useState<number | null>(null);

  useEffect(() => {
    (async () => {
      // fetch all and find by device_id to get pk
      const res = await api.get<any[]>('/devices/');
      const d = res.data.find((x) => x.device_id === device_id);
      if (d) {
        setDevicePk(d.id);
        setName(d.name);
        setGroup(d.group || '');
      }
    })();
  }, [device_id]);

  const sync = async () => {
    if (!devicePk) return;
    try {
      const res = await api.put(`/devices/${devicePk}/config`, { name, group: group || null });
      Alert.alert('Synced', 'Configuration updated');
    } catch (e: any) {
      Alert.alert('Error', e?.message || 'Sync failed');
    }
  };

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text variant="headlineSmall" style={{ marginBottom: 12 }}>Cloud Config Sync</Text>
      <TextInput label="Name" value={name} onChangeText={setName} style={{ marginBottom: 8 }} />
      <TextInput label="Group" value={group} onChangeText={setGroup} style={{ marginBottom: 16 }} />
      <Button mode="contained" onPress={sync}>Sync</Button>
    </View>
  );
}
