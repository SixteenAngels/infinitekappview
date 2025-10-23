import * as Sentry from '@sentry/react-native';
import Constants from 'expo-constants';

export function initSentry() {
  const dsn = Constants?.expoConfig?.extra?.SENTRY_DSN as string | undefined;
  if (!dsn) return;
  Sentry.init({
    dsn,
    tracesSampleRate: 0.2,
  });
}
