import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import api from '../api/api';

export default function OTAUpdate() {
  const [deviceId, setDeviceId] = useState('');
  const [version, setVersion] = useState('1.0.0');
  const [file, setFile] = useState<DocumentPicker.DocumentPickerAsset | null>(null);

  const pickFile = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: '*/*' });
    if (res.canceled) return;
    setFile(res.assets[0]);
  };

  const upload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append('device_id', deviceId);
    form.append('version', version);
    form.append('file', {
      uri: file.uri,
      name: file.name || 'firmware.bin',
      type: file.mimeType || 'application/octet-stream',
    } as any);

    try {
      await api.post('/ota/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } });
      Alert.alert('Success', 'OTA notification sent');
    } catch (e: any) {
      Alert.alert('Error', e?.message || 'Upload failed');
    }
  };

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 20, marginBottom: 12 }}>OTA Update</Text>
      <Text>Device ID</Text>
      <TextInput value={deviceId} onChangeText={setDeviceId} style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} />
      <Text>Version</Text>
      <TextInput value={version} onChangeText={setVersion} style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} />
      <Button title="Pick firmware" onPress={pickFile} />
      <View style={{ height: 8 }} />
      <Button title="Upload" onPress={upload} />
    </View>
  );
}
