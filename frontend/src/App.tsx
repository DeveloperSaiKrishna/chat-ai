import { BrowserRouter, Routes, Route } from "react-router-dom";
import LangChainChat from "./pages/LangChainChat";
import Chat from "./Chat";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/langchain-chat" element={<LangChainChat />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
