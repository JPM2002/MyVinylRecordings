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
    fetch("/api/albums")  // ✅ Use relative path (works with Vite proxy)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("🎵 Albums received:", data);
        setAlbums(data);
      })
      .catch((err) => {
        console.error("❌ Error fetching albums:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto text-white">
      <h1 className="text-3xl font-bold mb-6">🎵 My Vinyl Collection</h1>
      {loading ? <p>Loading albums...</p> : <AlbumGrid albums={albums} />}
    </div>
  );
}

export default Home;
