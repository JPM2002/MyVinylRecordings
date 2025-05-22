import { Link } from "react-router-dom";
import styles from "./AlbumList.module.css";

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

type Props = {
  albums: Album[];
};

function AlbumList({ albums }: Props) {
  return (
    <div className={styles.albumList}>
      {albums.map((album) => (
        <Link
          key={album.folder}
          to={`/album/${encodeURIComponent(album.folder)}`}
          className={styles.albumRow}
        >
          {album.cover && <img src={album.cover} alt={`${album.title} cover`} />}
          <div className={styles.albumInfo}>
            <h3>{album.title}</h3>
            <p>{album.artist}</p>
            <small>{album.metadata?.Released ?? "Year Unknown"} · {album.metadata?.Format}</small>
          </div>
        </Link>
      ))}
    </div>
  );
}

export default AlbumList;
