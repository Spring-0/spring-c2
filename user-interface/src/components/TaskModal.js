import React from 'react';
import TaskForm from './TaskForm';
import { AiOutlineClose } from 'react-icons/ai';

function TaskModal({ isOpen, onClose, onCreate }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg shadow-lg p-4 w-full max-w-md">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold">Create Task</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <AiOutlineClose size={24} />
                    </button>
                </div>
                <TaskForm onCreate={onCreate} />
            </div>
        </div>
    );
}

export default TaskModal;
