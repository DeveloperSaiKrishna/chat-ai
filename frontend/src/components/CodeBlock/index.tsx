import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import hljs from "highlight.js";
import "highlight.js/styles/github-dark.css";
import type { Components } from "react-markdown";
import { Code2Icon, CopyCheck, CopyIcon } from "lucide-react";

function CodeBlock({
    inline,
    className,
    children,
    ...props
}: React.ComponentPropsWithoutRef<"code"> & {
    inline?: boolean;
}) {
    const [copied, setCopied] = useState(false);
    const match = /language-(\w+)/.exec(className || "");
    const language = match?.[1];

    const codeString = String(children).replace(/\n$/, "");

    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(codeString);
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
        } catch (err) {
            console.error("Copy failed:", err);
        }
    };

    if (inline) {
        return (
            <code
                {...props}
                style={{
                    background: "#1e1e1e",
                    padding: "2px 4px",
                    borderRadius: "4px",
                }}
            >
                {children}
            </code>
        );
    }

    const refCallback = (node: HTMLElement | null) => {
        if (!node) return;

        const code = node.textContent || "";

        if (language && hljs.getLanguage(language)) {
            node.innerHTML = hljs.highlight(code, { language }).value;
        } else {
            node.innerHTML = hljs.highlightAuto(code).value;
        }
    };

    return (
        <div>
            <pre className="pre-code">
                <div className="mb-4 flex justify-between">
                    <div className="flex gap-4 items-center"><Code2Icon size={16} className="text-[6px]" />{language}</div>
                    <div onClick={copyToClipboard} className="rounded-full p-2 cursor-pointer hover:bg-black/10 transition-colors">
                        {copied ?
                            <CopyCheck
                                size={24}
                            // className="rounded-full cursor-pointer text-[black] hover:bg-black/10 transition-colors"
                            />
                            :
                            <CopyIcon
                                size={24}
                                className="text-[#bdbdbd]"
                            // className="p-1 rounded-md cursor-pointer text-[#bdbdbd] hover:bg-black/10 transition-colors"
                            />
                        }
                    </div>
                </div>
                <code
                    ref={refCallback}
                    className={language ? `language-${language}` : ""}
                    {...props}
                >
                    {codeString}
                </code>
            </pre>
        </div>
    );
}

const components: Components = {
    code: CodeBlock as any, // 👈 important TS escape hatch
};

export default function MarkdownRenderer({
    content,
}: {
    content: string;
}) {
    return (
        <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={components}
        >
            {content}
        </ReactMarkdown>
    );
}