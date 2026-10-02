import { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import type { Step } from "../services/api";
import { c, type } from "../utils/theme";

/** Steps the user can tick off. Tap a step to check it. */
export function StepList({ steps, accent = c.teal }: { steps: Step[]; accent?: string }) {
  const [done, setDone] = useState<Record<number, boolean>>({});
  return (
    <View>
      {steps.map((st, i) => (
        <Pressable key={i} onPress={() => setDone((d) => ({ ...d, [i]: !d[i] }))} style={s.row}
          accessibilityRole="checkbox" accessibilityState={{ checked: !!done[i] }} accessibilityLabel={st.title}>
          <View style={[s.box, { borderColor: accent }, done[i] && { backgroundColor: accent }]}>
            {done[i] ? <Text style={{ color: "#fff", fontWeight: "800" }}>✓</Text> : null}
          </View>
          <View style={{ flex: 1 }}>
            <Text style={[type.body, { fontWeight: "700" }, done[i] && { textDecorationLine: "line-through", color: c.muted }]}>{st.title}</Text>
            <Text style={type.small}>{st.detail}</Text>
          </View>
        </Pressable>
      ))}
    </View>
  );
}

const s = StyleSheet.create({
  row: { flexDirection: "row", gap: 12, paddingVertical: 12, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line },
  box: { width: 26, height: 26, borderRadius: 6, borderWidth: 2, alignItems: "center", justifyContent: "center", marginTop: 1 },
});