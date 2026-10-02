import { useEffect, useState } from "react";
import { Alert, Text, View } from "react-native";
import { Screen, P, Btn, ErrorText } from "../components/ui";
import { api, HistoryItem } from "../services/api";
import { kindLabel, timeAgo } from "../utils/format";
import { c, levelColor, type } from "../utils/theme";

export default function History() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [err, setErr] = useState<string>();

  const load = () => {
    setErr(undefined);

    api
      .getHistory()
      .then((data) => {
        setItems(data as HistoryItem[]);
      })
      .catch((e) => {
        setErr(e.message);
      });
  };

  useEffect(() => {
    load();
  }, []);

  const clear = () =>
    Alert.alert(
      "Delete all past checks?",
      "This also deletes saved recovery plans. It can't be undone.",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Delete all",
          style: "destructive",
          onPress: () =>
            api
              .clearHistory()
              .then(() => load())
              .catch((e) => setErr(e.message)),
        },
      ]
    );

  return (
    <Screen>
      <ErrorText msg={err} />

      {items.length === 0 && !err ? (
        <P muted>
          No checks yet. Check a link, message or screenshot and it will show
          up here.
        </P>
      ) : null}

      {items.map((it) => (
        <View
          key={it.id}
          style={{
            paddingVertical: 14,
            borderBottomWidth: 1,
            borderBottomColor: c.border,
          }}
        >
          <Text style={[type.body, { fontWeight: "700" }]}>
            {kindLabel(it.kind)}{" "}
            <Text style={{ color: levelColor(it.level) }}>
              {it.level} ({Math.round(it.score)})
            </Text>
          </Text>

          <Text style={type.small} numberOfLines={2}>
            {it.preview}
          </Text>

          <Text style={type.small}>
            {timeAgo(it.created_at)}
          </Text>
        </View>
      ))}

      {items.length > 0 ? (
        <View style={{ marginTop: 20 }}>
          <Btn
            label="Delete all past checks"
            kind="ghost"
            onPress={clear}
          />
        </View>
      ) : null}
    </Screen>
  );
}