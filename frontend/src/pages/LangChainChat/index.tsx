import {
  useMemo,
  useRef,
  useState,
  type ChangeEvent,
  type Dispatch,
  type SetStateAction,
} from "react";

import { Plus, Send } from "lucide-react";

import MarkdownRenderer from "../../components/CodeBlock";
import ModelsContianer from "../../components/ModelsContainer";
import ChatList from "../../components/ChatList";

type ChatsType = {
  id: number;
  q: string;
  a: string;
};

export type ChatWindowType = {
  id: number;
  chats: ChatsType[];
  model: string;
};

type ChatWindowProps = {
  id: number;
  chats: ChatsType[];
  setChatWindows: Dispatch<SetStateAction<ChatWindowType[]>>;
  selectedModel: string;
};

export const ChatWindow = ({
  id,
  chats,
  setChatWindows,
  selectedModel,
}: ChatWindowProps) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [showSendBtn, setShowSendBtn] = useState<boolean>(false);

  const handleInput = () => {
    const textarea = textareaRef.current;

    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;

      if (textareaRef.current) {
        setShowSendBtn(!!textareaRef.current.value);
      }
    }
  };

  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("Uploaded:", data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSend = async () => {
    const message = textareaRef.current?.value.trim();

    if (!message) return;

    const newChat: ChatsType = {
      id: Date.now(),
      q: message,
      a: "",
    };

    // add new chat
    setChatWindows((prev) =>
      prev.map((window) =>
        window.id === id
          ? {
              ...window,
              chats: [...window.chats, newChat],
            }
          : window,
      ),
    );

    if (textareaRef.current) {
      textareaRef.current.value = "";
      textareaRef.current.style.height = "auto";
    }

    try {
      const res = await fetch("http://localhost:8000/lang", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          model: selectedModel,
          session_id: id,
        }),
      });

      const reader = res.body?.getReader();

      if (!reader) return;

      const decoder = new TextDecoder();

      let fullText = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) break;

        fullText += decoder.decode(value, {
          stream: true,
        });

        requestAnimationFrame(() => {
          setChatWindows((prev) =>
            prev.map((window) => {
              if (window.id !== id) return window;

              const updatedChats = [...window.chats];

              updatedChats[updatedChats.length - 1] = {
                ...updatedChats[updatedChats.length - 1],
                a: fullText,
              };

              return {
                ...window,
                chats: updatedChats,
              };
            }),
          );
        });
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <div className="flex h-full w-[60vw] flex-col">
        {/* Messages */}

        <div className="flex-1 overflow-y-auto p-6 pb-40">
          <h1 className="text-center mb-2 text-2xl font-bold">
            LangChain with Session Memory
          </h1>
          <p className="leading-8 text-gray-900">
            {chats.length > 0
              ? chats.map((chat) => (
                  <div key={chat.id}>
                    {/* Question */}

                    <div className="mb-4 flex justify-end">
                      <div className="w-fit max-w-[30vw] rounded-lg bg-gray-100 px-4 py-2 text-right">
                        {chat.q}
                      </div>
                    </div>

                    {/* Answer */}

                    <div className="mb-4 flex">
                      <div className="w-fit max-w-full rounded-lg px-4 py-4 text-left">
                        <MarkdownRenderer content={chat.a || "Loading..."} />
                      </div>
                    </div>
                  </div>
                ))
              : "Chat here..."}
          </p>
        </div>

        {/* Input */}

        <div className="fixed bottom-0 w-[60vw] bg-white p-4">
          <div className="flex items-center gap-3 rounded-3xl border border-slate-300 bg-white px-2 py-2 shadow-lg">
            {/* hidden file input */}

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
            />

            {/* upload button */}

            <button
              onClick={handleFileClick}
              className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full bg-white transition hover:bg-gray-200"
            >
              <Plus size={20} />
            </button>

            {/* textarea */}

            <textarea
              ref={textareaRef}
              rows={1}
              onInput={handleInput}
              onKeyDown={(e) => {
                if (e.shiftKey && e.key === "Enter") return;
                if (e.key === "Enter") {
                  e.preventDefault();

                  handleSend();
                }
              }}
              placeholder="Message ChatGPT..."
              className="max-h-52 w-full flex-1 resize-none overflow-y-auto bg-transparent outline-none placeholder:text-gray-400"
            />

            {/* send button */}

            <div className="flex gap-1">
              {showSendBtn && (
                <button
                  onClick={handleSend}
                  className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full bg-white text-black transition hover:bg-gray-200"
                >
                  <Send size={18} />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

const initialId = Date.now();
const initialModel = "llama3";

const LangChainChat = () => {
  const [chatWindows, setChatWindows] = useState<ChatWindowType[]>([
    {
      id: initialId,
      model: initialModel,
      chats: [],
    },
  ]);
  const [activeChatWindowId, setActiveChatWindowId] = useState(initialId);

  const activeChat = useMemo(() => {
    return chatWindows.find(({ id }) => id === activeChatWindowId);
  }, [chatWindows, activeChatWindowId]);

  return (
    <div className="flex h-screen">
      <ChatList
        chatWindows={chatWindows}
        setChatWindows={setChatWindows}
        activeChatWindowId={activeChatWindowId}
        setActiveChatWindowId={setActiveChatWindowId}
      />

      {activeChat && (
        <ChatWindow
          key={activeChat.id}
          id={activeChat.id}
          chats={activeChat.chats}
          setChatWindows={setChatWindows}
          selectedModel={activeChat.model}
        />
      )}

      {activeChat && (
        <ModelsContianer
          selectedModel={activeChat.model}
          onSelectModel={(model) => {
            setChatWindows((pre) =>
              pre.map((window) => {
                if (window.id === activeChat.id) {
                  return {
                    ...window,
                    model: model,
                  };
                }
                return window;
              }),
            );
          }}
        />
      )}
    </div>
  );
};

export default LangChainChat;
