import { Link } from "react-router-dom";
import styles from "./AlbumCard.module.css";

type Album = {
  title: string;
  artist: string;
  folder: string;
  cover: string | null;
  metadata?: {
    Format?: string;
    Released?: number;
    CountryBought?: string;
  };
};

type Props = {
  album: Album;
};

function AlbumCard({ album }: Props) {
  const { title, artist, folder, cover, metadata = {} } = album;

  return (
    <Link to={`/album/${encodeURIComponent(folder)}`} className={styles.albumCard}>
      <img
        src={cover || "/default-cover.jpg"}
        alt={`${title} cover`}
        className={styles.albumImage}
        loading="lazy"
      />
      <div>
        <h3 className={styles.albumTitle}>{title}</h3>
        <p className={styles.albumArtist}>{artist}</p>

        {(metadata.Format || metadata.Released || metadata.CountryBought) && (
          <div className={styles.tagRow}>
            {metadata.Format && <span className={styles.tag}>{metadata.Format}</span>}
            {metadata.Released && <span className={styles.tag}>{metadata.Released}</span>}
            {metadata.CountryBought && <span className={styles.tag}>{metadata.CountryBought}</span>}
          </div>
        )}
      </div>
    </Link>
  );
}

export default AlbumCard;
