import AlbumCard from "./AlbumCard";
import "./AlbumGrid.css"; // Optional: add grid styles

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
    <div className="album-grid">
      {albums.map((album) => (
        <AlbumCard key={album.folder} album={album} />
      ))}
    </div>
  );
}

export default AlbumGrid;
