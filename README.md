# 🎵 My Vinyl Collection

A personal full-stack application to **organize, view, and enjoy your vinyl record collection** with rich metadata, album art, and dynamic UI modes.

---

## 🌟 Features

### 🧠 Smart Metadata Viewer
- Display album title, artist, year released, format, and country of purchase.
- Supports multiple audio formats: `mp3`, `flac`, `wav`, and `raw`.

### 🖼️ Beautiful Album Presentation
- **Grid View**: Classic card-style layout with album covers.
- **List View**: Lightweight row layout for quick scanning.

### 🎚️ Theme Switching
- Toggle between **Dark** and **Light** mode.
- Full CSS variable support for dynamic UI styling.

### 🔍 Search + Filters
- 🔎 **Search** by title or artist.
- 🎨 **Filter** by Format, Artist, and Country Bought.
- 🧠 React Select with theme-aware dropdown styling.

### 🎛️ Sorting
- Sort albums by:
  - Artist (A–Z, Z–A)
  - Title (A–Z, Z–A)
  - Year (Oldest–Newest, Newest–Oldest)

### 🔄 Animated Theme Transitions
- Smooth transitions when toggling between themes using `transition` on CSS variables.

---

## 📁 Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── AlbumCard.tsx
│   │   ├── AlbumGrid.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── AlbumList.tsx
│   ├── context/
│   │   └── ThemeContext.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
└── index.html
```

---

## 🧠 Technologies Used

- **Frontend**: React + TypeScript + Vite
- **Styling**: CSS Modules + CSS Variables
- **Theme Control**: React Context + DOM `data-theme` switching
- **Components**: `react-select` for dropdown filters
- **Media Handling**: `<audio>` element with embedded controls

---

## 🚀 Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/my-vinyl-collection.git
cd my-vinyl-collection
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start the Dev Server

```bash
npm run dev
```

---

## 🔧 Backend Support

This app expects a backend that:
- Serves album folders from a `/api/albums` endpoint
- Delivers cover art images
- Supports downloading formats as `.zip`

Example folder structure on backend:

```
Recordings/
└── Billy Joel - The Stranger/
    ├── Audio/
    │   ├── mp3/
    |   ├── flac/
    │   ├── raw/
    │   ├── wav/
    └── Front Cover/
    └── Back Cover/
    └── Fingerprint/
    └── metadata.json
```

---

## 🛠️ In Progress

- [ ] 🎞️ Album detail animations
- [ ] 💾 View mode persistence (via localStorage)
- [ ] 📥 Drag-and-drop upload of new albums
- [ ] 📊 Dashboard insights: formats, artists, years

---

## 🤝 Credits

Built with 💿 by [Javier Pozo Miranda](https://github.com/JPM2002)

Inspired by the love of analog music and personal libraries.

---

## 📄 License

to be decided...
