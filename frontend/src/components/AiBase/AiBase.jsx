import React, { Component } from "react";
import { NavLink as NavLinkAi, Outlet } from "react-router-dom";

import { useColorScheme } from "../../hooks/useColorThemeContext";
import { useSidebarState } from "../../hooks/useSidebarStateContext";

import UsersGearIcon from "../../svg_images/UsersGear.svg"
import ConfluenceIcon from "../../svg_images/Confluence.svg"
// import BareMetalIcon from "../../svg_images/BareMetal.svg"
import CatalogIcon from "../../svg_images/Catalog.svg"

const NavLink = React.forwardRef((props, ref) => {
  return (
    <NavLinkAi
      ref={ref}
      {...props}
      className={({ isActive }) =>
        isActive ? 'baseHref active' : 'baseHref'
      }
    />
  );
});

export default function AiBase() {
  const { colorScheme } = useColorScheme();
  const { sidebarCollapsed } = useSidebarState();

  return (
    <>
      <div className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
        <nav className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
          <NavLink to="/ai/summary" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Статус AI сервисов</div>
              ||
              <UsersGearIcon className="baseSidebarIcon"></UsersGearIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Статус AI сервисов</div>}
          </NavLink>
          <NavLink to="/ai/direct_llm" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Direct LLM</div>
              ||
              <UsersGearIcon className="baseSidebarIcon"></UsersGearIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Direct LLM</div>}
          </NavLink>
          <NavLink to="/ai/rag_llm" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">RAG LLM</div>
              ||
              <ConfluenceIcon className="baseSidebarIcon"></ConfluenceIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">RAG LLM</div>}
          </NavLink>
          <NavLink to="/ai/rag_docs" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Документы RAG</div>
              ||
              <CatalogIcon className="baseSidebarIcon"></CatalogIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Документы RAG</div>}
          </NavLink>
                    <NavLink to="/ai/llama_nodes" >
                      {!sidebarCollapsed &&
                        <div className="baseHrefText">Ноды LLAMA</div>
                        ||
                        <CatalogIcon className="baseSidebarIcon"></CatalogIcon>}
                      {sidebarCollapsed && <div className="baseSidebarTextDiv">Ноды LLAMA</div>}
                    </NavLink>
        </nav>
      </div>
      <div className={!sidebarCollapsed && "baseContent" || "baseContent collapsed"}>
        <Outlet />
      </div>
    </>
  );
}