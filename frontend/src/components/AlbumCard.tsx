import { Link } from "react-router-dom";
import styles from "./AlbumCard.module.css";

type Props = {
  album: {
    title: string;
    artist: string;
    folder: string;
    cover: string | null;
  };
};

function AlbumCard({ album }: Props) {
  return (
    <Link
      to={`/album/${encodeURIComponent(album.folder)}`}
      className={styles.albumCard}
    >
      <img
        src={album.cover || "/default-cover.jpg"}
        alt={`${album.title} cover`}
        className={styles.albumImage}
        loading="lazy"
      />
      <div>
        <h3 className={styles.albumTitle}>{album.title}</h3>
        <p className={styles.albumArtist}>{album.artist}</p>
      </div>
    </Link>
  );
}

export default AlbumCard;
