import { ReactNode } from "react";
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Switch, Text, TextInput, TextInputProps, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { c, type } from "../utils/theme";

export function Screen({ children, scroll = true }: { children: ReactNode; scroll?: boolean }) {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: c.paper }} edges={["bottom"]}>
      {scroll ? <ScrollView contentContainerStyle={s.pad} keyboardShouldPersistTaps="handled">{children}</ScrollView>
              : <View style={s.pad}>{children}</View>}
    </SafeAreaView>
  );
}

export const H1 = ({ children }: { children: ReactNode }) => <Text style={[type.display, { marginBottom: 8 }]}>{children}</Text>;
export const H2 = ({ children }: { children: ReactNode }) => <Text style={[type.h2, { marginTop: 24, marginBottom: 8 }]}>{children}</Text>;
export const P = ({ children, muted }: { children: ReactNode; muted?: boolean }) => <Text style={muted ? type.small : type.body}>{children}</Text>;

export function Btn({ label, onPress, kind = "primary", loading, disabled }:
  { label: string; onPress: () => void; kind?: "primary" | "danger" | "ghost"; loading?: boolean; disabled?: boolean }) {
  const bg = kind === "primary" ? c.teal : kind === "danger" ? c.critical : "transparent";
  const fg = kind === "ghost" ? c.teal : "#fff";
  return (
    <Pressable onPress={onPress} disabled={disabled || loading} accessibilityRole="button" accessibilityLabel={label}
      style={({ pressed }) => [s.btn, { backgroundColor: bg, opacity: disabled ? 0.45 : pressed ? 0.85 : 1 },
        kind === "ghost" && { borderWidth: 1.5, borderColor: c.teal }]}>
      {loading ? <ActivityIndicator color={fg} /> : <Text style={[s.btnText, { color: fg }]}>{label}</Text>}
    </Pressable>
  );
}

export function Field({ label, ...props }: { label: string } & TextInputProps) {
  return (
    <View style={{ marginBottom: 16 }}>
      <Text style={[type.small, { marginBottom: 6, color: c.ink, fontWeight: "600" }]}>{label}</Text>
      <TextInput placeholderTextColor={c.muted} {...props}
        style={[s.input, props.multiline && { minHeight: 140, textAlignVertical: "top" }, props.style]} />
    </View>
  );
}

export function Chips<T extends string>({ options, value, onChange }:
  { options: { value: T; label: string }[]; value?: T; onChange: (v: T) => void }) {
  return (
    <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
      {options.map((o) => {
        const on = o.value === value;
        return (
          <Pressable key={o.value} onPress={() => onChange(o.value)} accessibilityRole="button" accessibilityState={{ selected: on }}
            style={[s.chip, on && { backgroundColor: c.teal, borderColor: c.teal }]}>
            <Text style={{ color: on ? "#fff" : c.ink, fontWeight: "600" }}>{o.label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

export function ToggleRow({ label, hint, value, onChange }: { label: string; hint?: string; value: boolean; onChange: (v: boolean) => void }) {
  return (
    <View style={s.toggle}>
      <View style={{ flex: 1, paddingRight: 12 }}>
        <Text style={type.body}>{label}</Text>
        {hint ? <Text style={type.small}>{hint}</Text> : null}
      </View>
      <Switch value={value} onValueChange={onChange} trackColor={{ true: c.teal, false: c.line }} accessibilityLabel={label} />
    </View>
  );
}

export const ErrorText = ({ msg }: { msg?: string }) =>
  msg ? <Text style={{ color: c.critical, marginBottom: 12, fontSize: 15 }} accessibilityRole="alert">{msg}</Text> : null;

const s = StyleSheet.create({
  pad: { padding: 20, paddingBottom: 48 },
  btn: { minHeight: 52, borderRadius: 10, alignItems: "center", justifyContent: "center", paddingHorizontal: 18, marginTop: 8 },
  btnText: { fontSize: 17, fontWeight: "700" },
  input: { backgroundColor: c.surface, borderWidth: 1, borderColor: c.line, borderRadius: 10, padding: 14, fontSize: 16, color: c.ink },
  chip: { paddingVertical: 10, paddingHorizontal: 14, borderRadius: 20, borderWidth: 1, borderColor: c.line, backgroundColor: c.surface },
  toggle: { flexDirection: "row", alignItems: "center", paddingVertical: 12, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: c.line },
});