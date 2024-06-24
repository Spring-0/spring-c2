import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TaskTable from './components/TaskTable';

function App() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get("http://localhost:9393/api/get-tasks");
        setTasks(response.data);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, []);


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
      <h1 className="text-2xl font-bold mb-4">Task Table</h1>
      <TaskTable columns={taskColumns} data={tasks} />
    </div>
  );
}

export default App;