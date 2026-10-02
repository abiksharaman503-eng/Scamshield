import { Link } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Screen, H1, P } from "../components/ui";
import { c, type } from "../utils/theme";

const checks = [
  { href: "/url", title: "A link", hint: "Paste a web address or a QR code's link" },
  { href: "/message", title: "A message or email", hint: "SMS, WhatsApp, email text" },
  { href: "/screenshot", title: "A screenshot", hint: "Read the text and QR code in an image" },
  { href: "/account_check", title: "A profile or seller", hint: "Social media, dating, marketplace" },
] as const;

export default function Home() {
  return (
    <Screen>
      <H1>What reached you?</H1>
      <P muted>Choose what you want checked. Nothing is opened or clicked for you.</P>

      <View style={{ marginTop: 24 }}>
        {checks.map((x) => (
          <Link key={x.href} href={x.href} asChild>
            <Pressable style={s.row} accessibilityRole="button" accessibilityLabel={`Check ${x.title}`}>
              <View style={{ flex: 1 }}>
                <Text style={type.h2}>{x.title}</Text>
                <Text style={type.small}>{x.hint}</Text>
              </View>
              <Text style={s.chev}>›</Text>
            </Pressable>
          </Link>
        ))}
      </View>

      <Link href="/clicked" asChild>
        <Pressable style={s.alert} accessibilityRole="button" accessibilityLabel="Already clicked, shared details or lost money">
          <Text style={[type.h2, { color: c.critical }]}>Already clicked, shared something or lost money?</Text>
          <Text style={[type.small, { color: c.ink, marginTop: 4 }]}>Get a step-by-step recovery plan. The first hour matters.</Text>
        </Pressable>
      </Link>

      <Link href="/history" asChild>
        <Pressable style={{ marginTop: 24, padding: 8 }} accessibilityRole="link">
          <Text style={{ color: c.teal, fontWeight: "700", fontSize: 16 }}>See past checks</Text>
        </Pressable>
      </Link>
    </Screen>
  );
}

const s = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", paddingVertical: 18, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line },
  chev: { fontSize: 28, color: c.muted, paddingLeft: 12 },
  alert: { marginTop: 28, padding: 18, borderRadius: 12, backgroundColor: c.criticalSoft, borderLeftWidth: 5, borderLeftColor: c.critical },
});