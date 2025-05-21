import { useEffect, useState } from "react";
import AlbumGrid from "../components/AlbumGrid";
import styles from "./Home.module.css";

type Album = {
  title: string;
  artist: string;
  folder: string;
  cover: string | null;
};

function Home() {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetch("/api/albums")
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

  const filteredAlbums = albums.filter((album) =>
    (album.title + album.artist).toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className={styles.homeContainer}>
      <header className={styles.homeHeader}>
        <h1 className={styles.homeTitle}>
          <span className="icon">🎵</span> My Vinyl Collection
        </h1>
        <p className={styles.homeSubtitle}>Explore your favorite records</p>
      </header>

      <main>
        <div className={styles.searchBar}>
          <input
            type="text"
            placeholder="Search albums or artists..."
            className={styles.searchInput}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {loading ? (
          <p className={styles.loadingText}>Loading albums...</p>
        ) : filteredAlbums.length > 0 ? (
          <AlbumGrid albums={filteredAlbums} />
        ) : (
          <p className={styles.noAlbums}>No albums found.</p>
        )}
      </main>
    </div>
  );
}

export default Home;
