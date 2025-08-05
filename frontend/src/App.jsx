import React, { useState } from "react";
import axios from "axios";

export default function TranscriptionApp() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a video file");
    setLoading(true);
    setTranscript("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/transcribe/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTranscript(res.data.transcript);
    } catch (err) {
      console.error(err);
      alert("Failed to transcribe video");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-6 max-w-xl w-full">
        <h1 className="text-2xl font-bold mb-4">Video Transcription</h1>

        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {loading ? "Transcribing..." : "Upload & Transcribe"}
        </button>

        {transcript && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2">Transcript:</h2>
            <textarea
              value={transcript}
              readOnly
              rows={10}
              className="w-full p-2 border rounded"
            />
          </div>
        )}
      </div>
    </div>
  );
}
