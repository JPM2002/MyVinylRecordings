import { Link } from "react-router-dom";

type Props = {
  album: {
    title: string;
    artist: string;
    folder: string;
    cover: string | null;
  };
};

function AlbumCard({ album }: Props) {
  const coverUrl = album.cover
    ? `http://localhost:5000${album.cover}` // ✅ FIXED
    : "https://via.placeholder.com/150";

  return (
    <Link to={`/album/${encodeURIComponent(album.folder)}`} className="album-card">
      <img src={coverUrl} alt={album.title} />
      <h3>{album.title}</h3>
      <p>{album.artist}</p>
    </Link>
  );
}

export default AlbumCard;
