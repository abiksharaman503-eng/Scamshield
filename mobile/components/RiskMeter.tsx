import { StyleSheet, Text, View } from "react-native";
import { c, levelColor, type } from "../utils/theme";

const BANDS = [
  { level: "low", color: c.low, to: 25 }, { level: "medium", color: c.medium, to: 50 },
  { level: "high", color: c.high, to: 75 }, { level: "critical", color: c.critical, to: 100 },
];

/** Four-band strip with a marker at the score. The strip is the one distinctive element of the result screen. */
export function RiskMeter({ score, level, verdict, confidence }:
  { score: number; level: string; verdict: string; confidence: string }) {
  const col = levelColor(level);
  return (
    <View accessible accessibilityLabel={`${verdict}. Risk ${score} out of 100. Confidence ${confidence}.`}>
      <Text style={[type.display, { color: col }]}>{verdict}</Text>
      <View style={s.strip}>
        {BANDS.map((b) => <View key={b.level} style={{ flex: 1, backgroundColor: b.color, opacity: b.level === level ? 1 : 0.28 }} />)}
        <View style={[s.marker, { left: `${Math.min(Math.max(score, 1), 99)}%` }]} />
      </View>
      <View style={s.row}>
        <Text style={type.small}>Risk {score} / 100</Text>
        <Text style={type.small}>Confidence: {confidence}</Text>
      </View>
    </View>
  );
}

const s = StyleSheet.create({
  strip: { flexDirection: "row", height: 14, borderRadius: 7, overflow: "hidden", marginTop: 16, gap: 2 },
  marker: { position: "absolute", top: -3, bottom: -3, width: 4, marginLeft: -2, backgroundColor: c.ink, borderRadius: 2 },
  row: { flexDirection: "row", justifyContent: "space-between", marginTop: 8 },
});