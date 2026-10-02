import { useState } from "react";
import { useRouter } from "expo-router";
import { Screen, Btn, Chips, ErrorText, Field, H2, P, ToggleRow } from "../components/ui";
import { api } from "../services/api";
import { store } from "../services/store";

const FLAGS = [
  ["clicked_link", "I opened the link", undefined],
  ["entered_password", "I typed a password", undefined],
  ["entered_otp", "I shared or typed a one-time code (OTP)", undefined],
  ["entered_card_details", "I entered card details", "Number, expiry or CVV"],
  ["shared_id_documents", "I shared ID documents", "Aadhaar, PAN, passport, licence"],
  ["downloaded_file", "I downloaded a file", undefined],
  ["installed_app", "I installed an app", "Including an APK from a link"],
  ["gave_remote_access", "I let someone control my phone or computer", "AnyDesk, TeamViewer, screen sharing"],
  ["sent_money", "I sent money", undefined],
] as const;

export default function Clicked() {
  const router = useRouter();
  const [v, setV] = useState<Record<string, boolean>>({});
  const [method, setMethod] = useState<string>();
  const [amount, setAmount] = useState("");
  const [hours, setHours] = useState<number>();
  const [country, setCountry] = useState(store.country);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string>();

  const run = async () => {
    setBusy(true); setErr(undefined);
    store.country = country;
    try {
      store.plan = await api.assessIncident({
        ...v, scan_id: store.result?.id, country,
        payment_method: v.sent_money ? method : undefined,
        amount: v.sent_money && amount ? Number(amount) : undefined,
        hours_since: hours,
      });
      router.push("/recovery");
    } catch (e: any) { setErr(e.message); } finally { setBusy(false); }
  };

  return (
    <Screen>
      <P muted>Turn on everything that applies. It's fine if you're not sure. Nothing here is judged.</P>
      <H2>What did you do?</H2>
      {FLAGS.map(([k, label, hint]) => <ToggleRow key={k} label={label} hint={hint} value={!!v[k]} onChange={(x) => setV((p) => ({ ...p, [k]: x }))} />)}

      {v.sent_money ? (<>
        <H2>How did you pay?</H2>
        <Chips value={method} onChange={setMethod} options={[
          { value: "upi", label: "UPI" }, { value: "card", label: "Card" }, { value: "bank_transfer", label: "Bank transfer" },
          { value: "crypto", label: "Crypto" }, { value: "gift_card", label: "Gift card" }, { value: "other", label: "Other" }]} />
        <Field label="Amount (optional)" value={amount} onChangeText={setAmount} keyboardType="decimal-pad" />
      </>) : null}

      <H2>How long ago?</H2>
      <Chips value={hours === undefined ? undefined : String(hours)} onChange={(x) => setHours(Number(x))} options={[
        { value: "1", label: "Under 1 hour" }, { value: "24", label: "Today" }, { value: "72", label: "1 to 3 days" }, { value: "200", label: "Longer" }]} />

      <H2>Where are you?</H2>
      <Chips value={country} onChange={setCountry} options={[
        { value: "IN", label: "India" }, { value: "US", label: "USA" }, { value: "UK", label: "UK" },
        { value: "AU", label: "Australia" }, { value: "CA", label: "Canada" }, { value: "OTHER", label: "Other" }]} />

      <ErrorText msg={err} />
      <Btn label="Get my recovery plan" kind="danger" onPress={run} loading={busy} />
    </Screen>
  );
}