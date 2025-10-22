import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import api from '../api/api';

export default function RulesBuilder() {
  const [name, setName] = useState('High Temp Rule');
  const [conditions, setConditions] = useState('{"sensor":"temperature","op":">","value":28}');
  const [actions, setActions] = useState('{"topic":"infinitek/cmnd/fan","payload":{"state":"ON"}}');

  const createRule = async () => {
    try {
      await api.post('/rules', { name, conditions, actions });
      Alert.alert('Rule created');
    } catch (e: any) {
      Alert.alert('Error', e?.message || 'Failed to create rule');
    }
  };

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 20, marginBottom: 12 }}>Rules Builder</Text>
      <Text>Name</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} value={name} onChangeText={setName} />
      <Text>Conditions (JSON)</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 8 }} value={conditions} onChangeText={setConditions} multiline />
      <Text>Actions (JSON)</Text>
      <TextInput style={{ backgroundColor: '#eee', padding: 8, marginBottom: 16 }} value={actions} onChangeText={setActions} multiline />
      <Button title="Create Rule" onPress={createRule} />
    </View>
  );
}
