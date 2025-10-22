import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import { Text, Card } from 'react-native-paper';
import { LineChart } from 'react-native-chart-kit';
import api from '../api/api';

export default function SensorDashboard({ route }: any) {
  const { device_id } = route.params as { device_id: string };
  const [values, setValues] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);

  useEffect(() => {
    (async () => {
      const res = await api.get<any[]>('/measurements', {
        params: { device_id, sensor: 'temperature', limit: 20 },
      });
      const data = res.data.reverse();
      setValues(data.map((d) => d.value));
      setLabels(data.map((d) => new Date(d.created_at).toLocaleTimeString()));
    })();
  }, [device_id]);

  return (
    <View style={{ flex: 1, padding: 12 }}>
      <Text variant="titleLarge" style={{ marginBottom: 8 }}>Temperature</Text>
      <Card>
        <Card.Content>
          <LineChart
            data={{ labels, datasets: [{ data: values }] }}
            width={360}
            height={220}
            chartConfig={{
              backgroundGradientFrom: '#ffffff',
              backgroundGradientTo: '#ffffff',
              color: () => '#2a9d8f',
              labelColor: () => '#222',
            }}
            bezier
          />
        </Card.Content>
      </Card>
    </View>
  );
}
