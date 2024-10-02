import React, { useEffect, useState } from 'react'; 
import ReactMarkdown from 'react-markdown'; 
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'; 
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'; 
import { useNavigate } from 'react-router-dom'; 
import './MarkdownViewer.css'
 
export default function MarkdownViewer({ filePath }) { 
  const [markdownContent, setMarkdownContent] = useState(''); 
  const navigate = useNavigate(); 
 
  useEffect(() => { 
    fetch(filePath) 
      .then((response) => response.text()) 
      .then((text) => setMarkdownContent(text)); 
  }, [filePath]); 
 
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
 