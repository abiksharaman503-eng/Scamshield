const API_BASE_URL =
  process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000";

export type HistoryItem = {
  id: number;
  kind: string;
  level: string;
  score: number;
  preview: string;
  created_at: string;
};

type ApiResponse = Record<string, any>;

async function request(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  let data: ApiResponse;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      `Server returned an invalid response (${response.status})`
    );
  }

  if (!response.ok) {
    const detail = data?.detail ?? data?.message;

    let errorMessage = `Request failed with status ${response.status}`;

    if (typeof detail === "string") {
      errorMessage = detail;
    } else if (detail && typeof detail === "object") {
      errorMessage =
        detail.message ||
        detail.reason ||
        detail.error ||
        JSON.stringify(detail);
    }

    throw new Error(errorMessage);
  }

  return data;
}

export const api = {
  // ---------------- URL ----------------
  analyzeUrl(url: string) {
    return request("/api/url/analyze", {
      method: "POST",
      body: JSON.stringify({ url }),
    });
  },

  // ---------------- MESSAGE ----------------
  analyzeMessage(text: string) {
    return request("/api/message/analyze", {
      method: "POST",
      body: JSON.stringify({ text }),
    });
  },

  // ---------------- SCREENSHOT ----------------
  async analyzeScreenshot(imageUri: string) {
    const formData = new FormData();

    // Read selected image
    const imageResponse = await fetch(imageUri);

    if (!imageResponse.ok) {
      throw new Error("Could not read the selected image.");
    }

    // Convert image to Blob
    const blob = await imageResponse.blob();

    // Convert Blob to real File for Expo Web
    const file = new File(
      [blob],
      "screenshot.jpg",
      {
        type: blob.type || "image/jpeg",
      }
    );

    // FastAPI UploadFile expects multipart file
    formData.append("file", file);

    const response = await fetch(
      `${API_BASE_URL}/api/screenshot/analyze`,
      {
        method: "POST",
        body: formData,
      }
    );

    let data: ApiResponse;

    try {
      data = await response.json();
    } catch {
      throw new Error(
        `Server returned an invalid response (${response.status})`
      );
    }

    if (!response.ok) {
      const detail = data?.detail ?? data?.message;

      let errorMessage = `Request failed with status ${response.status}`;

      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (detail && typeof detail === "object") {
        errorMessage =
          detail.message ||
          detail.reason ||
          detail.error ||
          JSON.stringify(detail);
      }

      throw new Error(errorMessage);
    }

    return data;
  },

  // ---------------- ACCOUNT ----------------
  analyzeAccount(account: {
    platform: string;
    username: string;
    display_name?: string;
    bio?: string;
    followers?: number;
    following?: number;
    post_count?: number;
    account_age_days?: number;
    has_profile_photo?: boolean;
    asked_for_money?: boolean;
    moved_to_private_chat?: boolean;
    claims_investment_returns?: boolean;
    romantic_then_money?: boolean;
    profile_photo_reused?: boolean;
  }) {
    return request("/api/account/analyze", {
      method: "POST",
      body: JSON.stringify(account),
    });
  },

  // ---------------- INCIDENT ----------------
  assessIncident(incident: Record<string, any>) {
    return request("/api/incident/assess", {
      method: "POST",
      body: JSON.stringify(incident),
    });
  },

  // ---------------- REPORT ----------------
  async getIncidentReport(incidentId: number) {
    const response = await fetch(
      `${API_BASE_URL}/api/incident/${incidentId}/report`
    );

    if (!response.ok) {
      throw new Error(
        `Failed to get incident report (${response.status})`
      );
    }

    return response.text();
  },

  // ---------------- HISTORY ----------------
  getHistory() {
    return request("/api/history");
  },

  async clearHistory() {
    const response = await fetch(
      `${API_BASE_URL}/api/history`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error(
        `Failed to clear history (${response.status})`
      );
    }

    return response.json();
  },
};