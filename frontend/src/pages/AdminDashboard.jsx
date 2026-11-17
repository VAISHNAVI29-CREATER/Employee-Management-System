import { useState } from "react";
import EmployeeList from "../components/EmployeeList";
import EmployeeForm from "../components/EmployeeForm";

function AdminDashboard() {
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSaved = () => {
    setEditingEmployee(null);
    setRefreshKey((previous) => previous + 1);
  };

  return (
    <div className="container-fluid py-4">
      <div className="container">
        <div className="mb-4">
          <h2 className="fw-bold">Admin Dashboard</h2>
          <p className="text-muted">
            Manage employee records, departments and projects.
          </p>
        </div>

        <div className="card shadow-sm border-0 mb-4">
          <div className="card-body">
            <EmployeeForm
              editingEmployee={editingEmployee}
              onSaved={handleSaved}
              onCancel={() => setEditingEmployee(null)}
            />
          </div>
        </div>

        <div className="card shadow-sm border-0">
          <div className="card-body">
            <EmployeeList
              onEdit={setEditingEmployee}
              refreshKey={refreshKey}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;