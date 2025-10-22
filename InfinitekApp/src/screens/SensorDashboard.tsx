import React, { useEffect, useMemo, useRef, useState } from 'react';
import { View, useWindowDimensions, Platform } from 'react-native';
import { Text, Card } from 'react-native-paper';
import { LineChart } from 'react-native-chart-kit';
import api, { API_BASE } from '../api/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SensorDashboard({ route }: any) {
  const { device_id } = route.params as { device_id: string };
  const [values, setValues] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);
  const dim = useWindowDimensions();
  const chartWidth = Math.min(dim.width - 24, 800);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      // seed with recent data
      const res = await api.get<any[]>('/measurements', { params: { device_id, sensor: 'temperature', limit: 20 } });
      if (cancelled) return;
      const data = res.data.reverse();
      setValues(data.map((d) => d.value));
      setLabels(data.map((d) => new Date(d.created_at).toLocaleTimeString()));
      // live websocket
      const token = (await (await import('expo-secure-store')).getItemAsync('jwt_token')) || (await AsyncStorage.getItem('jwt_token'));
      const wsUrlBase = API_BASE.replace(/^http/, 'ws');
      const qs = token ? `?token=${encodeURIComponent(token)}` : '';
      const ws = new WebSocket(`${wsUrlBase}/ws/telemetry/${device_id}${qs}`);
      wsRef.current = ws;
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.sensor !== 'temperature' || typeof msg.value !== 'number') return;
          setValues((prev) => {
            const next = [...prev, msg.value];
            return next.slice(-50);
          });
          setLabels((prev) => {
            const next = [...prev, new Date().toLocaleTimeString()];
            return next.slice(-50);
          });
        } catch {}
      };
      ws.onerror = () => {};
      ws.onclose = () => {
        // naive reconnect
        setTimeout(() => {
          if (!cancelled) {
            // trigger effect by changing dep: use device_id only so we don't loop; manual retry not implemented here for brevity
          }
        }, 2000);
      };
    })();
    return () => {
      cancelled = true;
      if (wsRef.current) {
        try { wsRef.current.close(); } catch {}
        wsRef.current = null;
      }
    };
  }, [device_id]);

  return (
    <View style={{ flex: 1, padding: 12 }}>
      <Text variant="titleLarge" style={{ marginBottom: 8 }}>Temperature</Text>
      <Card>
        <Card.Content>
          <LineChart
            data={{ labels, datasets: [{ data: values }] }}
            width={chartWidth}
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
