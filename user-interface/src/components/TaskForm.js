import React, { useState } from 'react';

function TaskForm({ onCreate }) {
    const [formData, setFormData] = useState({
        client_id: '',
        command: '',
        command_mode: '',
        repeat_interval: '',
        run_once: false,
        target_path: '',
        execute: false
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onCreate(formData);
        setFormData({
            client_id: '',
            command: '',
            command_mode: '',
            repeat_interval: '',
            run_once: false,
            target_path: '',
            execute: false
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <input
                type="text"
                name="client_id"
                placeholder="Client ID"
                value={formData.client_id}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-lg w-full"
            />
            <input
                type="text"
                name="command"
                placeholder="Command"
                value={formData.command}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-lg w-full"
            />
            <select
                name="command_mode"
                value={formData.command_mode}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-lg w-full"
            >
                <option value="FUP">FUP</option>
                <option value="FDL">FDL</option>
                <option value="CMD">CMD</option>
                <option value="IMP">IMP</option>
            </select>
            <input
                type="number"
                name="repeat_interval"
                placeholder="Repeat Interval"
                value={formData.repeat_interval}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-lg w-full"
            />
            <input
                type="text"
                name="target_path"
                placeholder="Target Path"
                value={formData.target_path}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-lg w-full"
            />
            <div className="flex items-center">
                <input
                    type="checkbox"
                    name="run_once"
                    checked={formData.run_once}
                    onChange={handleChange}
                    className="mr-2"
                />
                <label>Run Once</label>
            </div>
            <div className="flex items-center">
                <input
                    type="checkbox"
                    name="execute"
                    checked={formData.execute}
                    onChange={handleChange}
                    className="mr-2"
                />
                <label>Execute</label>
            </div>
            <button type="submit" className="p-2 bg-blue-500 text-white rounded-lg">Create Task</button>
        </form>
    );
}

export default TaskForm;
