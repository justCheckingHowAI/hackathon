import { API_URL } from "@/lib/api";

interface CreateVapiCallParams {
  customerNumber: string;
  customerName?: string;
}

export async function createVapiCall({
  customerNumber,
  customerName,
}: CreateVapiCallParams): Promise<void> {
  const response = await fetch(`${API_URL}/vapi/calls`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      customerNumber,
      customerName,
    }),
  });

  if (!response.ok) {
    const payload = await response
      .json()
      .catch(() => ({ detail: "Could not queue the call." }));
    throw new Error(payload.detail ?? "Could not queue the call.");
  }
}
