import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AlbumDetail from "./pages/AlbumDetail";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/album/:albumId" element={<AlbumDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
