import { useState } from "react";
import { useRouter } from "expo-router";
import { Screen, Field, Btn, ErrorText, P } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";

export default function UrlScreen() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string>();

  const run = async () => {
    setBusy(true); setErr(undefined);
    try { store.result = await api.analyzeUrl(url.trim()); router.push("/result"); }
    catch (e: any) { setErr(e.message); } finally { setBusy(false); }
  };

  return (
    <Screen>
      <P muted>We study the address only. The page is never opened.</P>
      <Field label="Link" value={url} onChangeText={setUrl} placeholder="https://" autoCapitalize="none" autoCorrect={false} keyboardType="url" />
      <ErrorText msg={err} />
      <Btn label="Check this link" onPress={run} loading={busy} disabled={url.trim().length < 3} />
    </Screen>
  );
}