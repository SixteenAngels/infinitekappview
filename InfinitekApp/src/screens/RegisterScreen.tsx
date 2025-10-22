import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function RegisterScreen() {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const onSubmit = async () => {
    try {
      setLoading(true);
      await register(email.trim(), password);
    } catch (e: any) {
      Alert.alert('Registration failed', e?.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20, justifyContent: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Register</Text>
      <Text>Email</Text>
      <TextInput
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
        style={{ backgroundColor: '#eee', padding: 10, marginBottom: 12 }}
      />
      <Text>Password</Text>
      <TextInput
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{ backgroundColor: '#eee', padding: 10, marginBottom: 12 }}
      />
      <Button title={loading ? 'Loading...' : 'Register'} onPress={onSubmit} disabled={loading} />
    </View>
  );
}
