import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TaskTable from './components/TaskTable';
import TaskModal from './components/TaskModal';
import ConfirmDeleteDialog from './components/ConfirmDeleteDialog';

function App() {
  const [tasks, setTasks] = useState([]);
  const [isModalOpen, setModalOpen] = useState(false);
  const [isDeleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:9393/api/get-tasks");
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  const handleCreateTask = async (task) => {
    try {
      await axios.post("http://localhost:9393/api/write-task", task);
      fetchTasks();
      setModalOpen(false);
    } catch (error) {
      console.error("Error creating task:", error);
    }
  };

  const handleDeleteTask = async () => {
    if (!taskToDelete) return;
    try {
      await axios.delete(`http://localhost:9393/api/delete-task/${taskToDelete}`);
      fetchTasks();
      setDeleteDialogOpen(false);
      setTaskToDelete(null);
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  const taskColumns = React.useMemo(
    () => [
      { Header: "ID", accessor: "id" },
      { Header: "Client ID", accessor: "client_id" },
      { Header: "Command", accessor: "command" },
      { Header: "Command Mode", accessor: "command_mode" },
      { Header: "Execute", accessor: "execute" },
      { Header: "Next Execution", accessor: "next_execution" },
      { Header: "Target Path", accessor: "target_path" },
      { Header: "Run Once", accessor: "run_once" },
      { Header: "Repeat Interval", accessor: "repeat_interval" },
    ],
    []
  );

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Task Manager</h1>
      <button onClick={() => setModalOpen(true)} className="p-2 mb-4 bg-blue-500 text-white rounded-lg">
        Create Task
      </button>
      <TaskTable
        columns={taskColumns}
        data={tasks}
        onDelete={(taskId) => {
          setTaskToDelete(taskId);
          setDeleteDialogOpen(true);
        }}
      />
      <TaskModal
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        onCreate={handleCreateTask}
      />
      <ConfirmDeleteDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDeleteTask}
      />
    </div>
  );
}

export default App;
