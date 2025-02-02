import React, { Component } from "react";
import "./About.css";
import MarkdownViewer from "../MarkdownViewer/MarkdownViewer";

export default function About() {
    return (
        <div className="aboutMain">
            <MarkdownViewer filePath="/README.md" />
      </div>
    );
  
}
