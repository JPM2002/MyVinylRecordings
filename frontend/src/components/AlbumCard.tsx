import { Link } from "react-router-dom";
import "./AlbumCard.css";

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
      className="album-card"
    >
      <img
        src={album.cover || "/default-cover.jpg"}
        alt={`${album.title} cover`}
        className="album-cover"
        loading="lazy"
      />
      <div className="album-text">
        <h3 className="album-title">{album.title}</h3>
        <p className="album-artist">{album.artist}</p>
      </div>
    </Link>
  );
}

export default AlbumCard;
