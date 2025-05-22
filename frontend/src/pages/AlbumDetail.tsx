import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./AlbumDetail.module.css";

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
  downloadsAvailable: Record<string, boolean>;
};

function AlbumDetail() {
  const { folder } = useParams<{ folder: string }>();
  const [album, setAlbum] = useState<Album | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!folder) return;

    fetch(`/api/albums/${encodeURIComponent(folder)}`)
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

  if (loading) return <p className={styles.statusMessage}>Loading album...</p>;
  if (!album) return <p className={styles.statusError}>Album not found.</p>;

  const meta = album.metadata;
  const mp3Tracks = album.audio["mp3"] || [];
  const formats = ["mp3", "flac", "wav", "raw"];

  return (
    <div className={styles.albumDetailContainer}>
      <header>
        <h1 className={styles.albumTitle}>{meta.Title}</h1>
        <h2 className={styles.albumArtist}>{meta.Artist}</h2>
      </header>

      <section className={styles.albumMeta}>
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
        <div className={styles.albumCoverGrid}>
          {album.frontCover && (
            <img
              src={album.frontCover}
              alt="Front Cover"
              className={styles.albumCover}
            />
          )}
          {album.backCover && (
            <img
              src={album.backCover}
              alt="Back Cover"
              className={styles.albumCover}
            />
          )}
        </div>
      )}

      <div className={styles.downloadButtons}>
        {formats.map((format) => {
          const isAvailable = album.downloadsAvailable?.[format];
          const href = isAvailable ? `/api/download/${encodeURIComponent(album.folder)}/${format}` : "#";

          return (
            <a
              key={format}
              href={href}
              className={`${styles.downloadButton} ${!isAvailable ? styles.disabled : ""}`}
              onClick={(e) => {
                if (!isAvailable) e.preventDefault();
              }}
              download
            >
              {format.toUpperCase()}
            </a>
          );
        })}
      </div>

      {mp3Tracks.length > 0 && (
        <section className={styles.audioSection}>
          <h3>🎧 MP3 Tracks</h3>
          <ul>
            {mp3Tracks.map((track, index) => (
              <li key={index} className={styles.trackItem}>
                <p className={styles.trackTitle}>
                  {index + 1 < 10 ? "0" + (index + 1) : index + 1} – {track.title}
                </p>
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
