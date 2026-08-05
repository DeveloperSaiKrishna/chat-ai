import { BrowserRouter, Routes, Route } from "react-router-dom";
import LangChainChat from "./pages/LangChainChat";
import Chat from "./Chat";
import HealthAI from "./pages/HealthAI";
import NoteSearch from "./pages/NoteSearch";
import ImageToText from "./pages/ImageToText";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/langchain-chat" element={<LangChainChat />} />
        <Route path="/health-chat" element={<HealthAI />} />
        <Route path="/notes-search" element={<NoteSearch />} />
        <Route path="/image-to-text" element={<ImageToText />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
