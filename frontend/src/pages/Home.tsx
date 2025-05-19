import { useEffect, useState } from "react";
import AlbumGrid from "../components/AlbumGrid";

type Album = {
  title: string;
  artist: string;
  folder: string;
  cover: string | null;
};

function Home() {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/albums")
      .then((res) => res.json())
      .then((data) => {
        setAlbums(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching albums:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h1>🎵 My Vinyl Collection</h1>
      {loading ? <p>Loading albums...</p> : <AlbumGrid albums={albums} />}
    </div>
  );
}

export default Home;
