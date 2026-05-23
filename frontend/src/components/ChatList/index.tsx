import { type Dispatch, type SetStateAction } from "react";
import type { ChatWindowType } from "../../Chat";
import { CircleX } from "lucide-react";

type ChatListTypes = {
  chatWindows: ChatWindowType[];
  setChatWindows: Dispatch<SetStateAction<ChatWindowType[]>>;
  activeChatWindowId: number;
  setActiveChatWindowId: Dispatch<SetStateAction<number>>;
};

const ChatList = ({
  chatWindows,
  setChatWindows,
  activeChatWindowId,
  setActiveChatWindowId,
}: ChatListTypes) => {
  const handleNewChat = () => {
    const id = Date.now();
    const model = "llama3";

    setChatWindows((prev) => [
      ...prev,
      {
        id,
        chats: [],
        model: model,
      },
    ]);

    setActiveChatWindowId(id);
  };

  const handleDeleteChat = (chatId: number) => {
    // prevent deleting last chat

    if (chatWindows.length === 1) {
      return;
    }

    const updatedChats = chatWindows.filter((chat) => chat.id !== chatId);

    setChatWindows(updatedChats);

    // if active deleted -> switch

    if (activeChatWindowId === chatId) {
      setActiveChatWindowId(updatedChats[0].id);
    }
  };

  return (
    <div className="flex h-full w-[20vw] flex-col gap-4 border-r border-gray-200 p-4">
      {/* Header */}

      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Chat AI</h3>

        <button
          onClick={handleNewChat}
          className="cursor-pointer rounded-md bg-black px-3 py-2 text-sm text-white transition hover:bg-gray-800"
        >
          New Chat
        </button>
      </div>

      {/* Chat List */}

      <ul className="flex flex-col gap-2 overflow-y-auto">
        {chatWindows.map((chat) => (
          <li
            key={chat.id}
            className={`flex cursor-pointer items-center justify-between rounded-md p-3 transition ${
              chat.id === activeChatWindowId
                ? "bg-slate-300"
                : "bg-gray-100 hover:bg-gray-200"
            } `}
            onClick={() => setActiveChatWindowId(chat.id)}
          >
            <div className="truncate text-sm font-medium">Chat {chat.id}</div>

            <button
              onClick={(e) => {
                e.stopPropagation();

                handleDeleteChat(chat.id);
              }}
              className="cursor-pointer rounded px-2 py-1 text-xs hover:bg-black/10"
            >
              <CircleX />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatList;
