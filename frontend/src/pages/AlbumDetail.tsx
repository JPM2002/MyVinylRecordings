import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

type AudioFile = {
  title: string;
  file: string;
};

type Album = {
  folder: string;
  metadata: Record<string, string | number>;
  frontCover: string | null;
  backCover: string | null;
  audio: Record<string, AudioFile[]>;
};

function AlbumDetail() {
  const { folder } = useParams<{ folder: string }>();
  const [album, setAlbum] = useState<Album | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!folder) return;

    fetch(`/api/album/${encodeURIComponent(folder)}`)
      .then((res) => {
        if (!res.ok) throw new Error("Album not found");
        return res.json();
      })
      .then(setAlbum)
      .catch((err) => {
        console.error(err);
        setAlbum(null);
      })
      .finally(() => setLoading(false));
  }, [folder]);

  if (loading) return <p>Loading album...</p>;
  if (!album) return <p>Album not found.</p>;

  const meta = album.metadata;
  const mp3Tracks = album.audio["mp3"] || [];

  return (
    <div className="p-4 max-w-4xl mx-auto text-white">
      <h1 className="text-4xl font-bold">{meta.Title}</h1>
      <h2 className="text-xl mb-2">{meta.Artist}</h2>

      <p className="text-sm mb-2">
        <strong>Label:</strong> {meta.Label} | <strong>Released:</strong> {meta.Released} |{" "}
        <strong>Catalog#:</strong> {meta.CatalogNumber}
      </p>

      <p className="text-sm mb-2">
        <strong>Format:</strong> {meta.Format} | <strong>Country:</strong> {meta.CountryBought}
      </p>

      <p className="text-sm mb-4">
        <strong>Condition:</strong> Media – {meta.MediaCondition || "N/A"}, Sleeve –{" "}
        {meta.SleeveCondition || "N/A"}
        <br />
        <strong>Price Paid:</strong> {meta.PricePaid || "N/A"}
        <br />
        <strong>Notes:</strong> {meta.Notes || "None"}
      </p>

      {album.frontCover && (
        <img
          src={album.frontCover}
          alt="Front Cover"
          className="mb-4 rounded-lg shadow-lg max-w-md"
        />
      )}
      {album.backCover && (
        <img
          src={album.backCover}
          alt="Back Cover"
          className="mb-4 rounded-lg shadow-lg max-w-md"
        />
      )}

      {/* ✅ Show only MP3s here */}
      {mp3Tracks.length > 0 && (
        <div className="mb-6">
          <h3 className="text-xl font-semibold mb-2">MP3 Tracks</h3>
          <ul className="space-y-2">
            {mp3Tracks.map((track, index) => (
              <li key={index}>
                <p>{track.title}</p>
                <audio controls className="w-full mt-1">
                  <source src={track.file} type="audio/mp3" />
                  Your browser does not support the audio element.
                </audio>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 🔜 Future: download panel for FLAC/WAV/RAW */}
    </div>
  );
}

export default AlbumDetail;
