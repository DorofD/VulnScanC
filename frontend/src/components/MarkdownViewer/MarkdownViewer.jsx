import React, { useEffect, useState } from 'react'; 
import ReactMarkdown from 'react-markdown'; 
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'; 
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'; 
import { useNavigate } from 'react-router-dom'; 
import { useTimedMessagesContext } from '../../hooks/useTimedMessagesContext';
import './MarkdownViewer.css'
 
export default function MarkdownViewer({ filePath }) { 
  const [markdownContent, setMarkdownContent] = useState(''); 
  const navigate = useNavigate(); 
  const { addMessage } = useTimedMessagesContext();
 
  useEffect(() => { 
    fetch(filePath) 
      .then((response) => {
        if (!response.ok) {
          throw new Error('Не удалось загрузить файл');
        }
        return response.text();
      })
      .then((text) => setMarkdownContent(text))
      .catch((err) => {
        addMessage('Ошибка при загрузке Markdown: ' + err.message, 'error', 5000);
      });
  }, [filePath, addMessage]); 
 
  return ( 
    <div className='MarkdownMain'>
    <ReactMarkdown 
      children={markdownContent} 
      components={{ 
        a: ({ href, children }) => { 
          const isRelativeLink = !/^http/.test(href); 
          const handleClick = (e) => { 
            if (isRelativeLink) { 
              e.preventDefault(); 
              navigate(`/${href.replace(/\.md$/, '')}`);
            } 
          }; 
 
          return ( 
            <a href={href} onClick={handleClick}> 
              {children} 
            </a> 
          ); 
        }, 
        code({ node, inline, className, children, ...props }) { 
          const match = /language-(\w+)/.exec(className || ''); 
          return !inline && match ? ( 
            <SyntaxHighlighter 
              style={atomDark} 
              language={match[1]} 
              PreTag="div" 
              {...props} 
            > 
              {String(children).replace(/\n$/, '')} 
            </SyntaxHighlighter> 
          ) : ( 
            <code className={className} {...props}> 
              {children} 
            </code> 
          ); 
        } 
      }} 
    /> 
    </div>
  ); 
}; 
 