import { useState } from "react";
import { useRouter } from "expo-router";
import { Screen, Field, Btn, ErrorText, ToggleRow, H2, P } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";

const num = (v: string) => (v.trim() === "" || isNaN(+v) ? undefined : Math.round(+v));

export default function AccountCheck() {
  const router = useRouter();
  const [f, setF] = useState({ platform: "", username: "", bio: "", followers: "", following: "", posts: "", ageDays: "" });
  const [flags, setFlags] = useState({ asked_for_money: false, moved_to_private_chat: false, claims_investment_returns: false,
    romantic_then_money: false, profile_photo_reused: false });
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string>();
  const set = (k: keyof typeof f) => (v: string) => setF((p) => ({ ...p, [k]: v }));
  const flag = (k: keyof typeof flags) => (v: boolean) => setFlags((p) => ({ ...p, [k]: v }));

  const run = async () => {
    setBusy(true); setErr(undefined);
    try {
      store.result = await api.analyzeAccount({
        platform: f.platform || undefined, username: f.username || undefined, bio: f.bio || undefined,
        followers: num(f.followers), following: num(f.following), post_count: num(f.posts), account_age_days: num(f.ageDays), ...flags,
      });
      router.push("/result");
    } catch (e: any) { setErr(e.message); } finally { setBusy(false); }
  };

  return (
    <Screen>
      <P muted>Fill in what you can see. Blank fields are skipped.</P>
      <Field label="Platform" value={f.platform} onChangeText={set("platform")} placeholder="Instagram, WhatsApp, OLX" />
      <Field label="Username" value={f.username} onChangeText={set("username")} autoCapitalize="none" />
      <Field label="Bio" value={f.bio} onChangeText={set("bio")} multiline />
      <Field label="Followers" value={f.followers} onChangeText={set("followers")} keyboardType="number-pad" />
      <Field label="Following" value={f.following} onChangeText={set("following")} keyboardType="number-pad" />
      <Field label="Number of posts" value={f.posts} onChangeText={set("posts")} keyboardType="number-pad" />
      <Field label="Account age in days" value={f.ageDays} onChangeText={set("ageDays")} keyboardType="number-pad" />
      <H2>What have they done?</H2>
      <ToggleRow label="Asked me for money or gift cards" value={flags.asked_for_money} onChange={flag("asked_for_money")} />
      <ToggleRow label="Moved the chat to a private app" value={flags.moved_to_private_chat} onChange={flag("moved_to_private_chat")} />
      <ToggleRow label="Promised guaranteed investment returns" value={flags.claims_investment_returns} onChange={flag("claims_investment_returns")} />
      <ToggleRow label="Became romantic fast, then asked for money" value={flags.romantic_then_money} onChange={flag("romantic_then_money")} />
      <ToggleRow label="Profile photo appears under another name" value={flags.profile_photo_reused} onChange={flag("profile_photo_reused")} />
      <ErrorText msg={err} />
      <Btn label="Check this profile" onPress={run} loading={busy} />
    </Screen>
  );
}