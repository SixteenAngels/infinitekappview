import React, { useEffect, useState } from 'react';
import { View, RefreshControl } from 'react-native';
import { FAB, Text } from 'react-native-paper';
import { useWindowDimensions } from 'react-native';
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

  const dim = useWindowDimensions();
  const containerPadding = Math.max(12, (dim.width - 600) / 2);
  return (
    <View style={{ flex: 1, paddingHorizontal: containerPadding, paddingVertical: 12 }}>
      <Text variant="titleLarge" style={{ marginBottom: 8 }}>Devices</Text>
      <View style={{ flex: 1 }}>
        <View style={{ flex: 1 }}>
          {/* @ts-expect-error RN FlatList import inline to preserve control */}
          <require('react-native').FlatList
            data={devices}
            keyExtractor={(d: any) => String(d.id)}
            renderItem={({ item }: any) => (
              <DeviceCard
                device={item}
                onDashboard={() => nav.navigate('SensorDashboard', { device_id: item.device_id })}
                onSync={() => nav.navigate('DeviceSync', { device_id: item.device_id })}
              />
            )}
            refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
          />
        </View>
      </View>
      <FAB icon="plus" style={{ position: 'absolute', right: 16, bottom: 16 }} onPress={() => nav.navigate('AddDeviceScreen')} />
    </View>
  );
}
