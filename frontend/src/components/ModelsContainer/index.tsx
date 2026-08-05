type ModelContainerTypes = {
  selectedModel: string;
  onSelectModel: (model: string) => void;
};

const MODELS = [
  {
    id: "llama3",
    title: "Llama 3",
  },
  {
    id: "qwen2.5:7b",
    title: "Qwen 2.5",
  },
  {
    id: "qwen2.5vl:latest",
    title: "Qwen 2.5vl - Image",
  },
];

const ModelsContianer = ({
  selectedModel,
  onSelectModel,
}: ModelContainerTypes) => {
  return (
    <div className="flex h-full flex-col p-4 border-l border-gray-200">
      <h3 className="mb-4 text-xl font-medium">Select LLM:</h3>
      <ul className="flex flex-col gap-2">
        {MODELS.map(({ id, title }) => (
          <li
            key={id}
            className={`rounded-sm p-2 ${id === selectedModel ? "bg-slate-400" : "bg-gray-200"}`}
            onClick={() => onSelectModel(id)}
          >
            {title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ModelsContianer;
