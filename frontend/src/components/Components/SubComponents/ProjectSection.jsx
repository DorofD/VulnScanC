import React from "react";
import ProjectCard from "../../../Projects/ProjectCard/ProjectCard";

const ProjectSection = ({ 
    projects, 
    loadingProjects, 
    pickedProject, 
    onProjectClick 
}) => {
    return (
        <div className="componentsProjects">
            <p>Проекты</p>
            {loadingProjects === 'loading' && <div className="loader-placeholder">Loading projects...</div>}
            {loadingProjects === 'error' && <p> бекенд отвалился</p>}
            {loadingProjects === 'loaded' && (
                <>
                    {projects.map(project => (
                        <ProjectCard 
                            key={project.id}
                            id={project.id}
                            name={project.name}
                            picked={pickedProject.id === project.id}
                            onClick={() => onProjectClick(project)}
                        />
                    ))}
                </>
            )}
        </div>
    );
};

export default ProjectSection;
