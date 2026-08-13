import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

interface MarkdownViewerProps {
  content: string;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  return (
    <div className="prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-800 prose-code:font-mono prose-code:text-slate-200 text-sm text-slate-200">
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          h1: ({ children }) => <h1 className="text-lg font-semibold text-slate-100 mt-4 mb-2">{children}</h1>,
          h2: ({ children }) => <h2 className="text-base font-semibold text-slate-100 mt-3 mb-2">{children}</h2>,
          h3: ({ children }) => <h3 className="text-sm font-semibold text-slate-200 mt-3 mb-1">{children}</h3>,
          p: ({ children }) => <p className="mb-3 leading-relaxed text-slate-200">{children}</p>,
          ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-3 text-slate-300">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 mb-3 text-slate-300">{children}</ol>,
          li: ({ children }) => <li className="text-slate-200">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-slate-600 pl-3 py-1 my-2 bg-slate-900/50 text-slate-300 italic text-xs">
              {children}
            </blockquote>
          ),
          code: ({ className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            return match ? (
              <code className="block bg-[#0D121D] p-3 rounded-lg border border-slate-800 text-slate-200 font-mono text-xs overflow-x-auto my-2" {...props}>
                {children}
              </code>
            ) : (
              <code className="bg-slate-900 border border-slate-800 px-1.5 py-0.5 rounded text-slate-200 font-mono text-xs" {...props}>
                {children}
              </code>
            );
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
