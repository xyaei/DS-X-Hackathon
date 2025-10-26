export async function uploadResume(file: File) {
  const form = new FormData();
  form.append("resume", file); // must match FastAPI param name

  const res = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `Upload failed (${res.status})`);
  }
  return res.json() as Promise<{
    ok: boolean;
    filename: string;
    pages: number;
    first_page_text: string;
    all_pages: { page: number; text: string }[];
  }>;
}
