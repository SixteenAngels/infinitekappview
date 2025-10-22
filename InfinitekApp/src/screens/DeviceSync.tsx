import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
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
      <Text style={{ fontSize: 20, marginBottom: 12 }}>Cloud Config Sync</Text>
      <Text>Name</Text>
      <TextInput value={name} onChangeText={setName} style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} />
      <Text>Group</Text>
      <TextInput value={group} onChangeText={setGroup} style={{ backgroundColor: '#eee', padding: 8, marginBottom: 16 }} />
      <Button title="Sync" onPress={sync} />
    </View>
  );
}
