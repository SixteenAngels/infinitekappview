import React, { useState } from 'react';
import { View, Alert } from 'react-native';
import { Text, TextInput, Button } from 'react-native-paper';
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
      <Text variant="headlineSmall" style={{ marginBottom: 12 }}>Add Device</Text>
      <TextInput label="Name" style={{ marginBottom: 8 }} value={name} onChangeText={setName} />
      <TextInput label="Device ID" style={{ marginBottom: 8 }} value={deviceId} onChangeText={setDeviceId} />
      <TextInput label="Group (optional)" style={{ marginBottom: 16 }} value={group} onChangeText={setGroup} />
      <Button mode="contained" onPress={onSubmit}>Create</Button>
    </View>
  );
}
