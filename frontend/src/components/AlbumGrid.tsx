import AlbumCard from "./AlbumCard";
import styles from "./AlbumGrid.module.css";

type Props = {
  albums: {
    title: string;
    artist: string;
    folder: string;
    cover: string | null;
  }[];
};

function AlbumGrid({ albums }: Props) {
  return (
    <div className={styles.albumGrid}>
      {albums.map((album) => (
        <AlbumCard key={album.folder} album={album} />
      ))}
    </div>
  );
}

export default AlbumGrid;
