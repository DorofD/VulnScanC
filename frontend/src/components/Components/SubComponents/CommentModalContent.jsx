import React from "react";
import Button from "../../../components/Button/Button";
import CommentCard from "../../../components/Components/CommentCard/CommentCard";

const CommentModalContent = ({
    componentComments,
    userName,
    pickedComment,
    onPickedComment,
    onDeleteComponentComment,
    componentComment,
    setComponentComment,
    onAddComponentComment,
    pickedComponentId
}) => {
    return (
        <div className="changeModalComments">Комментарии
            <div className="comments">
                {componentComments.map(comment => (
                    <CommentCard
                        key={comment.id}
                        id={comment.id}
                        onClick={() => { if (pickedComment.id !== comment.id) { onPickedComment(comment) } else { onPickedComment({ id: '' }) } }}
                        picked={pickedComment.id === comment.id}
                        user={comment.user_name}
                        datetime={comment.datetime}
                        deleteFunction={() => onDeleteComponentComment()}
                        owner={comment.user_name === userName}
                    />
                ))}
            </div>
            <textarea className="comments" id={pickedComponentId} placeholder='Комментарий' value={componentComment.comment} onChange={e => setComponentComment({ ...componentComment, comment: e.target.value })}></textarea>
            <div className="sendLogo">
                <img src="" alt="" className="sendLogo" onClick={onAddComponentComment} />
            </div>
        </div>
    );
};

export default CommentModalContent;
