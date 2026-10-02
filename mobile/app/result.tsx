import { useRouter } from "expo-router";
import { Text, View } from "react-native";
import { Screen, H2, P, Btn } from "../components/ui";
import { RiskMeter } from "../components/RiskMeter";
import { store } from "../services/store";
import { c, levelColor, type } from "../utils/theme";

function safeText(value: any): string {
  if (value === null || value === undefined) return "";

  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }

  if (typeof value === "object") {
    if (value.reason) return String(value.reason);
    if (value.message) return String(value.message);
    if (value.text) return String(value.text);
    if (value.url) return String(value.url);
    if (value.payload) return String(value.payload);

    return JSON.stringify(value);
  }

  return String(value);
}

export default function ResultScreen() {
  const router = useRouter();
  const r = store.result;

  if (!r) {
    return (
      <Screen>
        <P>No result yet. Go back and run a check.</P>
      </Screen>
    );
  }

  const reasons = Array.isArray(r.reasons) ? r.reasons : [];
  const urls = Array.isArray(r.urls) ? r.urls : [];

  return (
    <Screen>
      <RiskMeter
        score={r.score}
        level={r.level}
        verdict={r.verdict}
        confidence={r.confidence}
      />

      <H2>Why we think so</H2>

      {reasons.length === 0 ? (
        <P muted>
          We found nothing unusual. That doesn't prove it's safe.
        </P>
      ) : (
        reasons.map((reason: any, index: number) => (
          <View
            key={index}
            style={{
              flexDirection: "row",
              marginBottom: 12,
            }}
          >
            <View
              style={{
                width: 8,
                height: 8,
                borderRadius: 4,
                backgroundColor: levelColor(r.level),
                marginTop: 7,
                marginRight: 10,
              }}
            />

            <Text style={[type.body, { flex: 1 }]}>
              {safeText(reason)}
            </Text>
          </View>
        ))
      )}

      {urls.length > 0 ? (
        <>
          <H2>Links inside</H2>

          {urls.map((item: any, index: number) => (
            <View key={index} style={{ marginBottom: 10 }}>
              <Text style={type.small}>
                <Text
                  style={{
                    color: levelColor(item?.level),
                    fontWeight: "700",
                  }}
                >
                  {safeText(item?.level)} ({safeText(item?.score)})
                </Text>
              </Text>

              <Text style={type.body}>
                {safeText(item)}
              </Text>
            </View>
          ))}
        </>
      ) : null}

      {r.qr ? (
        <>
          <H2>QR code</H2>
          <P>{safeText(r.qr?.payload || r.qr)}</P>
        </>
      ) : null}

      {r.extracted_text ? (
        <>
          <H2>Extracted text</H2>
          <Text
            selectable
            style={[
              type.small,
              {
                backgroundColor: c.card,
                padding: 12,
                borderRadius: 8,
              },
            ]}
          >
            {safeText(r.extracted_text)}
          </Text>
        </>
      ) : null}

      {r.disclaimer ? (
        <View style={{ marginTop: 16 }}>
          <P muted>{safeText(r.disclaimer)}</P>
        </View>
      ) : null}

      <View style={{ marginTop: 24 }}>
        {Number(r.score) >= 25 ? (
          <Btn
            label="I already clicked or shared something"
            kind="danger"
            onPress={() => router.push("/clicked")}
          />
        ) : null}

        <Btn
          label="Check something else"
          kind="ghost"
          onPress={() => router.dismissAll()}
        />
      </View>
    </Screen>
  );
}