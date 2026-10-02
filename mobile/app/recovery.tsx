import { useRouter } from "expo-router";
import { Text, View } from "react-native";
import { Screen, H2, P, Btn } from "../components/ui";
import { StepList } from "../components/StepList";
import { store } from "../services/store";
import { c, levelColor, type } from "../utils/theme";

export default function Recovery() {
  const router = useRouter();
  const p = store.plan;
  if (!p) return <Screen><P>No plan yet. Answer the questions first.</P></Screen>;
  const col = p.urgency === "low" ? c.low : p.urgency === "high" ? c.high : c.critical;

  return (
    <Screen>
      <Text style={[type.display, { color: col }]}>{p.headline}</Text>

      <H2>What may be exposed</H2>
      {p.exposures.map((e, i) => (
        <View key={i} style={{ marginBottom: 10 }}>
          <Text style={type.body}><Text style={{ fontWeight: "700", color: levelColor(e.severity === "low" ? "low" : e.severity) }}>{e.item}. </Text>{e.why}</Text>
        </View>
      ))}

      <H2>Do these now</H2>
      <StepList steps={p.do_now} accent={c.critical} />
      {p.within_24h.length ? (<><H2>Within 24 hours</H2><StepList steps={p.within_24h} /></>) : null}
      {p.this_week.length ? (<><H2>This week</H2><StepList steps={p.this_week} /></>) : null}

      <View style={{ marginTop: 24 }}>
        <Btn label="Report it and get an evidence pack" onPress={() => router.push("/report")} />
      </View>
    </Screen>
  );
}