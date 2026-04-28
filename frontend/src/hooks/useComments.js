import { useState, useEffect } from "react";
import { apiGetComponentComments, apiAddComponentComment, apiDeleteComponentComment } from "../services/apiComments";
import { useTimedMessagesContext } from "../hooks/useTimedMessagesContext";

export function useComments(componentId, userId) {
    const [componentComments, setComponentComments] = useState([{ id: 0 }]);
    const [componentComment, setComponentComment] = useState({ user_id: userId, comment: '' });
    const [pickedComment, setPickedComment] = useState({ id: '' });
    const { addMessage } = useTimedMessagesContext();
    
    async function getComponentComments(id) {
        try {
            const comments = await apiGetComponentComments(id);
            setComponentComments(comments);
        } catch (err) {
            addMessage(`Проблема с бекендом: ${err}`, 'error', 5000);
            setComponentComments([{ id: 0 }]);
        }
    }

    async function addComponentComment() {
        if (componentComment.comment === '') {
            addMessage('Введите комментарий', 'warning', 3000);
            return 1;
        }
        try {
            const response = await apiAddComponentComment(userId, componentId, componentComment.comment);
            if (response.status === 200) {
                getComponentComments(componentId);
                addMessage('Комментарий добавлен', 'success', 3000);
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            } else {
                addMessage('Не удалось добавить комментарий', 'error', 3000);
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error}`, 'error', 5000);
            setComponentComment({ user_id: userId, comment: '' });
            setPickedComment({ id: '' });
        }
    }

    async function deleteComponentComment() {
        try {
            const response = await apiDeleteComponentComment(pickedComment.id);
            if (response.status === 200) {
                getComponentComments(componentId);
                addMessage('Комментарий удален', 'success', 3000);
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            } else {
                addMessage('Не удалось удалить комментарий', 'error', 3000);
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error}`, 'error', 5000);
            setComponentComment({ user_id: userId, comment: '' });
            setPickedComment({ id: '' });
        }
    }

    useEffect(() => {
        if (componentId) {
            getComponentComments(componentId);
        }
    }, [componentId]);

    return {
        componentComments,
        componentComment,
        setComponentComment,
        pickedComment,
        setPickedComment,
        addComponentComment,
        deleteComponentComment,
        getComponentComments
    };
}
