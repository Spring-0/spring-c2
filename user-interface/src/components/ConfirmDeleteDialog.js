import React from 'react';
import { AiOutlineClose } from 'react-icons/ai';

function ConfirmDeleteDialog({ isOpen, onClose, onConfirm }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg shadow-lg p-4 w-full max-w-sm">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold">Confirm Deletion</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <AiOutlineClose size={24} />
                    </button>
                </div>
                <p>Are you sure you want to delete this task?</p>
                <div className="flex justify-end mt-4 space-x-2">
                    <button onClick={onClose} className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400">
                        Cancel
                    </button>
                    <button onClick={onConfirm} className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
                        Delete
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ConfirmDeleteDialog;