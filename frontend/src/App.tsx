import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AlbumDetail from "./pages/AlbumDetail";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/album/:folder" element={<AlbumDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
