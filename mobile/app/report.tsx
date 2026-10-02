import { useEffect, useState } from "react";
import { ActivityIndicator, Linking, Share, Text, View } from "react-native";
import { Screen, H2, P, Btn, ErrorText } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";
import { c, type } from "../utils/theme";

export default function Report() {
  const p = store.plan;
  const [pack, setPack] = useState<string>();
  const [err, setErr] = useState<string>();

  useEffect(() => {
    if (!p) return;
    api.getIncidentReport(p.incident_id).then(setPack).catch((e) => setErr(e.message));
  }, []);

  if (!p) return <Screen><P>No incident yet. Get a recovery plan first.</P></Screen>;

  return (
    <Screen>
      <H2>Where to report</H2>
      {p.report.map((r) => (
        <View key={r.name} style={{ marginBottom: 14 }}>
          <Text style={[type.body, { fontWeight: "700" }]}>{r.name}</Text>
          <Text style={type.small}>{r.how}</Text>
          <View style={{ flexDirection: "row", gap: 12 }}>
            {r.phone ? <Btn label={`Call ${r.phone}`} kind="ghost" onPress={() => Linking.openURL(`tel:${r.phone!.replace(/\s/g, "")}`)} /> : null}
            {r.url ? <Btn label="Open website" kind="ghost" onPress={() => Linking.openURL(r.url!)} /> : null}
          </View>
        </View>
      ))}

      <H2>Evidence pack</H2>
      <P muted>Give this summary to your bank or the police. Fill in the blanks marked (add) from your receipts.</P>
      {!pack && !err ? <ActivityIndicator style={{ marginTop: 16 }} color={c.teal} /> : null}
      <ErrorText msg={err} />
      {pack ? (<>
        <View style={{ backgroundColor: c.surface, borderRadius: 10, padding: 14, marginTop: 12, borderWidth: 1, borderColor: c.line }}>
          <Text selectable style={{ fontFamily: "Courier", fontSize: 12, color: c.ink }}>{pack}</Text>
        </View>
        <Btn label="Share or save this summary" onPress={() => Share.share({ message: pack, title: "Scam incident summary" })} />
      </>) : null}

      <H2>Stay safe next time</H2>
      {p.prevent.map((t, i) => <Text key={i} style={[type.body, { marginBottom: 8 }]}>{t}</Text>)}
    </Screen>
  );
}