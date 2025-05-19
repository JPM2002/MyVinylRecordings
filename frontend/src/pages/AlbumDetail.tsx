import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./AlbumDetail.css";

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
        console.error("Error loading album:", err);
        setAlbum(null);
      })
      .finally(() => setLoading(false));
  }, [folder]);

  if (loading) return <p className="status-message">Loading album...</p>;
  if (!album) return <p className="status-error">Album not found.</p>;

  const meta = album.metadata;
  const mp3Tracks = album.audio["mp3"] || [];

  return (
    <div className="album-detail-container">
      <header>
        <h1 className="album-title">{meta.Title}</h1>
        <h2 className="album-artist">{meta.Artist}</h2>
      </header>

      <section className="album-meta">
        <p>
          <strong>Label:</strong> {meta.Label} | <strong>Released:</strong>{" "}
          {meta.Released} | <strong>Catalog#:</strong> {meta.CatalogNumber}
        </p>
        <p>
          <strong>Format:</strong> {meta.Format} | <strong>Country:</strong>{" "}
          {meta.CountryBought}
        </p>
        <p>
          <strong>Condition:</strong> Media – {meta.MediaCondition || "N/A"},
          Sleeve – {meta.SleeveCondition || "N/A"}
        </p>
        <p>
          <strong>Price Paid:</strong> {meta.PricePaid || "N/A"}
        </p>
        <p>
          <strong>Notes:</strong> {meta.Notes || "None"}
        </p>
      </section>

      {(album.frontCover || album.backCover) && (
        <div className="album-cover-grid">
          {album.frontCover && (
            <img
              src={album.frontCover}
              alt="Front Cover"
              className="album-cover"
            />
          )}
          {album.backCover && (
            <img
              src={album.backCover}
              alt="Back Cover"
              className="album-cover"
            />
          )}
        </div>
      )}

      {mp3Tracks.length > 0 && (
        <section className="audio-section">
          <h3>🎧 MP3 Tracks</h3>
          <ul>
            {mp3Tracks.map((track, index) => (
              <li key={index} className="track-item">
                <p className="track-title">{track.title}</p>
                <audio controls>
                  <source src={track.file} type="audio/mp3" />
                  Your browser does not support the audio element.
                </audio>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

export default AlbumDetail;
