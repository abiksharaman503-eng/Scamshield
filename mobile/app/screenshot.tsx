import { useState } from "react";
import { Image } from "react-native";
import { useRouter } from "expo-router";
import * as ImagePicker from "expo-image-picker";
import { Screen, Btn, ErrorText, P } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";

export default function ScreenshotScreen() {
  const router = useRouter();
  const [uri, setUri] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string>();

  const pick = async () => {
    const r = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ["images"], quality: 0.8 });
    if (!r.canceled) { setUri(r.assets[0].uri); setErr(undefined); }
  };
  const run = async () => {
    if (!uri) return;
    setBusy(true); setErr(undefined);
    try { store.result = await api.analyzeScreenshot(uri); router.push("/result"); }
    catch (e: any) { setErr(e.message); } finally { setBusy(false); }
  };

  return (
    <Screen>
      <P muted>We read the text and any QR code in the image. Crop out anything private first.</P>
      {uri ? <Image source={{ uri }} style={{ height: 260, borderRadius: 10, marginVertical: 16 }} resizeMode="contain" accessibilityLabel="Selected screenshot" /> : null}
      <Btn label={uri ? "Choose a different image" : "Choose an image"} onPress={pick} kind={uri ? "ghost" : "primary"} />
      <ErrorText msg={err} />
      {uri ? <Btn label="Check this screenshot" onPress={run} loading={busy} /> : null}
    </Screen>
  );
}