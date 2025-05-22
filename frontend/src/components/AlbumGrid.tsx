import AlbumCard from "./AlbumCard";
import styles from "./AlbumGrid.module.css";

type Props = {
  albums: {
    title: string;
    artist: string;
    folder: string;
    cover: string | null;
    metadata?: {
      Format?: string;
      Released?: number;
      CountryBought?: string;
    };
  }[];
};

function AlbumGrid({ albums }: Props) {
  return (
    <div className={styles.albumGrid}>
      {albums.map((album) => (
        <AlbumCard
          key={album.folder}
          album={{
            ...album,
            metadata: album.metadata || {}, // ensure fallback
          }}
        />
      ))}
    </div>
  );
}

export default AlbumGrid;
