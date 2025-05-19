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
  return (
    <Link
      to={`/album/${encodeURIComponent(album.folder)}`}
      className="album-card"
    >
      <img
        src={album.cover || "/default-cover.jpg"}
        alt={`${album.title} cover`}
        className="album-cover"
      />
      <h3>{album.title}</h3>
      <p>{album.artist}</p>
    </Link>
  );
}

export default AlbumCard;
