import { useEffect, useState } from "react";
import AlbumGrid from "../components/AlbumGrid";
import styles from "./Home.module.css";

type Album = {
  title: string;
  artist: string;
  folder: string;
  cover: string | null;
};

type SortOption = "title-asc" | "title-desc" | "artist-asc" | "artist-desc";

function Home() {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
 const [sortOption, setSortOption] = useState<SortOption>("artist-asc");


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

  const handleSort = (a: Album, b: Album): number => {
    const key = sortOption.startsWith("title") ? "title" : "artist";
    const order = sortOption.endsWith("desc") ? -1 : 1;
    return a[key].localeCompare(b[key]) * order;
  };

  const filteredAlbums = albums
    .filter(
      (album) =>
        album.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        album.artist.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort(handleSort);

  return (
    <div className={styles.homeContainer}>
      <header className={styles.homeHeader}>
        <h1 className={styles.homeTitle}>
          <span className="icon">🎵</span> My Vinyl Collection
        </h1>
        <p className={styles.homeSubtitle}>Explore your favorite records</p>

        <div className={styles.controls}>
          <input
            type="text"
            placeholder="Search albums or artists..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.searchInput}
          />

          <select
            className={styles.sortDropdown}
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value as SortOption)}
          >
            <option value="artist-asc">Artist (A–Z)</option>
            <option value="artist-desc">Artist (Z–A)</option>
            <option value="title-asc">Title (A–Z)</option>
            <option value="title-desc">Title (Z–A)</option>
          </select>
        </div>
      </header>

      <main>
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
