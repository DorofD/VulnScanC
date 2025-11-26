import React from "react";
import { Routes, Route } from "react-router-dom"
import Base from "./Base/Base"
import Projects from "./Projects/Projects"
import Components from "./Components/Components";
import Snapshots from "./Snapshots/Snapshots";
import BduFstec from "./BduFstec/BduFstec";
import DependencyTrack from "./DependencyTrack/DependencyTrack";
import Admin from "./Admin/Admin"
import About from "./About/About"
import Users from "./Users/Users";
import Logs from "./Logs/Logs";
import MarkdownViewer from "./MarkdownViewer/MarkdownViewer";
import Binary from "./Binary/Binary";
import SarifViewer from "./Sarif/Sarif";
import Bitbake from "./Bitbake/Bitbake";
import Login from "./Login/Login";
import { PrivateRoute } from "./PrivateRoute/PrivateRoute";
import { useAuthContext } from "../hooks/useAuthContext";
import "./App.css";
import "./Button/Button.css";
import '../color_themes/App-themes-links.css';
export default function App() {
    const { userRole } = useAuthContext()
    return (
        <>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route element={<PrivateRoute />}>
                    <Route path="/" element={<Base />}>
                        <Route index element={<Projects />} />
                        <Route path="/components" element={<Components />} />
                        <Route path="/bdu_fstec" element={<BduFstec />} />
                        <Route path="/snapshots" element={<Snapshots />} />
                        <Route path="/bitbake" element={<Bitbake />} />
                        <Route path="/dependencyTrack" element={<DependencyTrack />} />
                        <Route path="/sarif" element={<SarifViewer />} />
                        {userRole === 'admin' && <Route path="/admin" element={<Admin />}>
                            <Route path="/admin/users" element={<Users />} />
                            <Route path="/admin/binary" element={<Binary />} />
                            <Route path="/admin/logs" element={<Logs />} />
                        </Route>}

                        <Route path="/about" element={<About />} />
                        <Route path="/README" element={<About />} />
                        <Route path="/docs/installation" element={<MarkdownViewer filePath="/docs/installation.md" />} />
                        <Route path="/docs/ci_integration" element={<MarkdownViewer filePath="/docs/ci_integration.md" />} />
                        <Route path="/docs/search_mechanism" element={<MarkdownViewer filePath="/docs/search_mechanism.md" />} />
                        <Route path="/search_mechanism" element={<MarkdownViewer filePath="/docs/search_mechanism.md" />} />
                        <Route path="/docs/web_ui" element={<MarkdownViewer filePath="/docs/web_ui.md" />} />
                        <Route path="/docs/executable_module" element={<MarkdownViewer filePath="/docs/executable_module.md" />} />
                        <Route path="/executable_module" element={<MarkdownViewer filePath="/docs/executable_module.md" />} />

                        <Route path="/web_ui" element={<MarkdownViewer filePath="/docs/web_ui.md" />} />
                        <Route path="/docs/ui_instructions/projects" element={<MarkdownViewer filePath="/docs/ui_instructions/projects.md" />} />
                        <Route path="/docs/ui_instructions/components" element={<MarkdownViewer filePath="/docs/ui_instructions/components.md" />} />
                        <Route path="/docs/ui_instructions/snapshots" element={<MarkdownViewer filePath="/docs/ui_instructions/snapshots.md" />} />
                        <Route path="/docs/ui_instructions/svacer" element={<MarkdownViewer filePath="/docs/ui_instructions/svacer.md" />} />
                        <Route path="/docs/ui_instructions/administration" element={<MarkdownViewer filePath="/docs/ui_instructions/administration.md" />} />
                        <Route path="/docs/ui_instructions/bdu" element={<MarkdownViewer filePath="/docs/ui_instructions/bdu.md" />} />
                        <Route path="/docs/ui_instructions/bitbake" element={<MarkdownViewer filePath="/docs/ui_instructions/bitbake.md" />} />
                        <Route path="/docs/ui_instructions/dt" element={<MarkdownViewer filePath="/docs/ui_instructions/dt.md" />} />
                        <Route path="/docs/ui_instructions/sarif" element={<MarkdownViewer filePath="/docs/ui_instructions/sarif.md" />} />
                    </Route>
                </Route>
            </Routes>
        </>
    );
}
