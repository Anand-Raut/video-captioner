import React, { useState } from "react";
import axios from "axios";

export default function TranscriptionApp() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a video file");
    setLoading(true);
    setTranscript("");
    setDownloadUrl("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/transcribe/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTranscript(res.data.transcript);
      setDownloadUrl(`http://localhost:8000${res.data.download_url}`);
    } catch (err) {
      console.error(err);
      alert("Failed to transcribe video");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">🎥 Video Transcriber</h1>

        <div className="space-y-4">
          <input
            type="file"
            accept="video/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 disabled:bg-blue-400 transition duration-200"
          >
            {loading ? "Transcribing..." : "Upload & Transcribe"}
          </button>
        </div>

        {transcript && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">📝 Transcript:</h2>
            <textarea
              value={transcript}
              readOnly
              rows={10}
              className="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 font-mono text-sm resize-none"
            />
          </div>
        )}

        {downloadUrl && (
          <div className="mt-4 text-center">
            <a
              href={downloadUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 text-blue-600 font-semibold hover:underline"
            >
              ⬇️ Download Video with Subtitles
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
