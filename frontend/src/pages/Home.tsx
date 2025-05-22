import { useEffect, useState } from "react";
import AlbumGrid from "../components/AlbumGrid";
import styles from "./Home.module.css";
import Select from "react-select";
import { useTheme } from "../context/ThemeContext";

type Album = {
  title: string;
  artist: string;
  folder: string;
  cover: string | null;
  metadata: {
    Format?: string;
    Released?: number;
    CountryBought?: string;
  };
};

type SortOption = "title-asc" | "title-desc" | "artist-asc" | "artist-desc" | "year-asc" | "year-desc";

function Home() {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOption, setSortOption] = useState<SortOption>("artist-asc");

  const [formatOptions, setFormatOptions] = useState<string[]>([]);
  const [selectedFormats, setSelectedFormats] = useState<string[]>([]);

  const [artistOptions, setArtistOptions] = useState<string[]>([]);
  const [selectedArtist, setSelectedArtist] = useState<string | null>(null);

  const [countryOptions, setCountryOptions] = useState<string[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null);

  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    fetch("/api/albums")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        return res.json();
      })
      .then((data: Album[]) => {
        setAlbums(data);

        const formats = new Set<string>();
        const artists = new Set<string>();
        const countries = new Set<string>();

        data.forEach((album) => {
          album.metadata?.Format?.split(",").forEach((f) => {
            const trimmed = f.trim();
            if (trimmed) formats.add(trimmed);
          });
          if (album.artist) artists.add(album.artist);
          if (album.metadata?.CountryBought) countries.add(album.metadata.CountryBought);
        });

        setFormatOptions(Array.from(formats).sort());
        setArtistOptions(Array.from(artists).sort());
        setCountryOptions(Array.from(countries).sort());
      })
      .catch((err) => console.error("❌ Error fetching albums:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleSort = (a: Album, b: Album): number => {
    const order = sortOption.endsWith("desc") ? -1 : 1;
    if (sortOption.startsWith("title")) return a.title.localeCompare(b.title) * order;
    if (sortOption.startsWith("artist")) return a.artist.localeCompare(b.artist) * order;
    if (sortOption.startsWith("year")) {
      const yearA = a.metadata.Released || 0;
      const yearB = b.metadata.Released || 0;
      return (yearA - yearB) * order;
    }
    return 0;
  };

  const filteredAlbums = albums
    .filter((album) => {
      const matchesSearch =
        album.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        album.artist.toLowerCase().includes(searchTerm.toLowerCase());

      const albumFormats = album.metadata?.Format?.split(",").map((f) => f.trim()) || [];
      const matchesFormat =
        selectedFormats.length === 0 ||
        selectedFormats.some((format) => albumFormats.includes(format));

      const matchesArtist = !selectedArtist || album.artist === selectedArtist;
      const matchesCountry =
        !selectedCountry || album.metadata.CountryBought === selectedCountry;

      return matchesSearch && matchesFormat && matchesArtist && matchesCountry;
    })
    .sort(handleSort);

  return (
    <div className={styles.homeContainer}>
      <header className={styles.homeHeader}>
        <h1 className={styles.homeTitle}>
          <span className="icon">🎵</span> My Vinyl Collection
        </h1>
        <p className={styles.homeSubtitle}>Explore your favorite records</p>
        <button onClick={toggleTheme} className={styles.themeToggle}>
  {theme === "dark" ? "🌞 Light" : "🌙 Dark"}
</button>

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
            <option value="year-asc">Year (Oldest–Newest)</option>
            <option value="year-desc">Year (Newest–Oldest)</option>
          </select>

          <div className={styles.multiSelectWrapper}>
            <Select
              isMulti
              placeholder="Filter by format..."
              options={formatOptions.map((format) => ({ value: format, label: format }))}
              onChange={(selected) => setSelectedFormats(selected.map((s) => s.value))}
              classNamePrefix="reactSelect"
              className="reactSelect"
              theme={(theme) => ({
                ...theme,
                colors: {
                  ...theme.colors,
                  primary25: "#374151",
                  primary: "#4f46e5",
                  neutral0: "#1f1f1f",
                  neutral5: "#1f1f1f",
                  neutral10: "#374151",
                  neutral20: "#4f46e5",
                  neutral30: "#4f46e5",
                  neutral80: "#f9fafb",
                },
              })}
            />
          </div>

          <button
            onClick={() => setShowAdvancedFilters((prev) => !prev)}
            className={styles.advancedToggle}
          >
            ⋯
          </button>
        </div>

        {showAdvancedFilters && (
          <div className={styles.advancedFilters}>
            <Select
              isClearable
              placeholder="Filter by Country Bought"
              options={countryOptions.map((c) => ({ value: c, label: c }))}
              onChange={(selected) => setSelectedCountry(selected?.value || null)}
              className="reactSelect"
              classNamePrefix="reactSelect"
              theme={(theme) => ({
                ...theme,
                colors: {
                  ...theme.colors,
                  primary25: "#374151",
                  primary: "#4f46e5",
                  neutral0: "#1f1f1f",
                  neutral5: "#1f1f1f",
                  neutral10: "#374151",
                  neutral20: "#4f46e5",
                  neutral30: "#4f46e5",
                  neutral80: "#f9fafb",
                },
              })}
            />

            <Select
              isClearable
              placeholder="Filter by Artist"
              options={artistOptions.map((a) => ({ value: a, label: a }))}
              onChange={(selected) => setSelectedArtist(selected?.value || null)}
              className="reactSelect"
              classNamePrefix="reactSelect"
              theme={(theme) => ({
                ...theme,
                colors: {
                  ...theme.colors,
                  primary25: "#374151",
                  primary: "#4f46e5",
                  neutral0: "#1f1f1f",
                  neutral5: "#1f1f1f",
                  neutral10: "#374151",
                  neutral20: "#4f46e5",
                  neutral30: "#4f46e5",
                  neutral80: "#f9fafb",
                },
              })}
            />
          </div>
        )}
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
