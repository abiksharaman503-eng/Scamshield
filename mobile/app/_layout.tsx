import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { c } from "../utils/theme";

export default function Layout() {
  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerStyle: { backgroundColor: c.paper }, headerShadowVisible: false, headerTintColor: c.ink,
        headerTitleStyle: { fontWeight: "700" }, contentStyle: { backgroundColor: c.paper }, headerBackTitle: "Back" }}>
        <Stack.Screen name="index" options={{ title: "ScamShield" }} />
        <Stack.Screen name="url" options={{ title: "Check a link" }} />
        <Stack.Screen name="message" options={{ title: "Check a message" }} />
        <Stack.Screen name="screenshot" options={{ title: "Check a screenshot" }} />
        <Stack.Screen name="account-check" options={{ title: "Check a profile" }} />
        <Stack.Screen name="result" options={{ title: "Result" }} />
        <Stack.Screen name="clicked" options={{ title: "What happened?" }} />
        <Stack.Screen name="recovery" options={{ title: "Recovery plan" }} />
        <Stack.Screen name="report" options={{ title: "Report and evidence" }} />
        <Stack.Screen name="history" options={{ title: "Past checks" }} />
      </Stack>
    </>
  );
}