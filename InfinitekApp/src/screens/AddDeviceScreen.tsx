import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import api from '../api/api';

export default function AddDeviceScreen() {
  const [name, setName] = useState('');
  const [deviceId, setDeviceId] = useState('');
  const [group, setGroup] = useState('');

  const onSubmit = async () => {
    try {
      await api.post('/devices/', { name, device_id: deviceId, group: group || null });
      Alert.alert('Success', 'Device added');
    } catch (e: any) {
      Alert.alert('Error', e?.message || 'Failed to add device');
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 20, marginBottom: 12 }}>Add Device</Text>
      <Text>Name</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} value={name} onChangeText={setName} />
      <Text>Device ID</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} value={deviceId} onChangeText={setDeviceId} />
      <Text>Group (optional)</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 16 }} value={group} onChangeText={setGroup} />
      <Button title="Create" onPress={onSubmit} />
    </View>
  );
}
