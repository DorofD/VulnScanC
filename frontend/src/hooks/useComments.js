import { useState, useEffect } from "react";
import { apiGetComponentComments, apiAddComponentComment, apiDeleteComponentComment } from "../services/apiComments";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";

export function useComments(componentId, userId) {
    const [componentComments, setComponentComments] = useState([{ id: 0 }]);
    const [componentComment, setComponentComment] = useState({ user_id: userId, comment: '' });
    const [pickedComment, setPickedComment] = useState({ id: '' });
    const { messages, addMessage } = useTimedMessagesContext();
    
    async function getComponentComments(id) {
        try {
            const comments = await apiGetComponentComments(id);
            setComponentComments(comments);
        } catch (err) {
            notificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' });
            toggleNotificationFunc();
            setComponentComments([{ id: 0 }]);
        }
    }

    async function addComponentComment() {
        if (componentComment.comment === '') {
            notificationData({ message: 'Введите комментарий', type: 'error' });
            toggleNotificationFunc();
            return 1;
        }
        try {
            const response = await apiAddComponentComment(userId, componentId, componentComment.comment);
            if (response.status === 200) {
                getComponentComments(componentId);
                notificationData({ message: 'Комментарий добавлен', type: 'success' });
                toggleNotificationFunc();
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            } else {
                notificationData({ message: 'Не удалось добавить комментарий', type: 'error' });
                toggleNotificationFunc();
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            }
        } catch (error) {
            notificationData({ message: `Проблема с бекендом: ${error}`, type: 'error' });
            toggleNotificationFunc();
            setComponentComment({ user_id: userId, comment: '' });
            setPickedComment({ id: '' });
        }
    }

    async function deleteComponentComment() {
        try {
            const response = await apiDeleteComponentComment(pickedComment.id);
            if (response.status === 200) {
                getComponentComments(componentId);
                notificationData({ message: 'Комментарий удален', type: 'success' });
                toggleNotificationFunc();
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            } else {
                notificationData({ message: 'Не удалось удалить комментарий', type: 'error' });
                toggleNotificationFunc();
                setComponentComment({ user_id: userId, comment: '' });
                setPickedComment({ id: '' });
            }
        } catch (error) {
            notificationData({ message: `Проблема с бекендом: ${error}`, type: 'error' });
            toggleNotificationFunc();
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
