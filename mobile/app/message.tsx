import { useState } from "react";
import { useRouter } from "expo-router";
import { Screen, Field, Btn, ErrorText, P } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";

export default function MessageScreen() {
  const router = useRouter();
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string>();

  const run = async () => {
    setBusy(true); setErr(undefined);
    try { store.result = await api.analyzeMessage(text.trim()); router.push("/result"); }
    catch (e: any) { setErr(e.message); } finally { setBusy(false); }
  };

  return (
    <Screen>
      <P muted>Paste the whole message. Links inside it are checked too. Codes and card numbers are hidden before anything is saved.</P>
      <Field label="Message" value={text} onChangeText={setText} multiline placeholder="Paste the message here" />
      <ErrorText msg={err} />
      <Btn label="Check this message" onPress={run} loading={busy} disabled={text.trim().length < 3} />
    </Screen>
  );
}