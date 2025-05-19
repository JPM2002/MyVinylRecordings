import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../components/AlbumGrid.css";

type Album = {
  folder: string;
  title: string;
  artist: string;
  cover: string | null;
};

function AlbumList() {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/albums")
      .then((res) => res.json())
      .then(setAlbums)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading albums...</p>;
  if (albums.length === 0) return <p>No albums found.</p>;

  return (
    <div className="album-grid">
      {albums.map((album) => (
        <Link
          key={album.folder}
          to={`/album/${encodeURIComponent(album.folder)}`}
          className="album-card"
        >
          <img
            src={album.cover || "/default-cover.jpg"}
            alt={album.title}
            className="album-cover"
          />
          <h3>{album.title}</h3>
          <p>{album.artist}</p>
        </Link>
      ))}
    </div>
  );
}

export default AlbumList;
