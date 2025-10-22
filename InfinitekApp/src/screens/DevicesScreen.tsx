import React, { useEffect, useState } from 'react';
import { View, FlatList, Button, RefreshControl } from 'react-native';
import api from '../api/api';
import DeviceCard, { Device } from '../components/DeviceCard';
import { useNavigation } from '@react-navigation/native';

export default function DevicesScreen() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const nav = useNavigation<any>();

  const load = async () => {
    const res = await api.get<Device[]>('/devices/');
    setDevices(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  };

  return (
    <View style={{ flex: 1, padding: 12 }}>
      <FlatList
        data={devices}
        keyExtractor={(d) => String(d.id)}
        renderItem={({ item }) => (
          <DeviceCard
            device={item}
            onDashboard={() => nav.navigate('SensorDashboard', { device_id: item.device_id })}
            onSync={() => nav.navigate('DeviceSync', { device_id: item.device_id })}
          />
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      />
      <Button title="Add Device" onPress={() => nav.navigate('AddDeviceScreen')} />
    </View>
  );
}
